using UnityEngine;
using Cinemachine;

namespace StormRunner
{
    public class CameraController : MonoBehaviour
    {
        [Header("Camera Settings")]
        [SerializeField] private CinemachineVirtualCamera virtualCamera;
        [SerializeField] private Transform target;
        [SerializeField] private float mouseSensitivity = 2f;
        [SerializeField] private float smoothTime = 0.1f;
        
        [Header("Camera Distance")]
        [SerializeField] private float minDistance = 2f;
        [SerializeField] private float maxDistance = 8f;
        [SerializeField] private float currentDistance = 5f;
        [SerializeField] private float zoomSpeed = 2f;
        
        [Header("Camera Angles")]
        [SerializeField] private float minVerticalAngle = -30f;
        [SerializeField] private float maxVerticalAngle = 60f;
        
        [Header("Collision Detection")]
        [SerializeField] private LayerMask collisionLayers = 1;
        [SerializeField] private float collisionRadius = 0.2f;
        
        private CinemachineComposer composer;
        private CinemachineTransposer transposer;
        private float currentRotationX;
        private float currentRotationY;
        private Vector3 currentVelocity;
        
        private void Awake()
        {
            if (virtualCamera == null)
                virtualCamera = GetComponent<CinemachineVirtualCamera>();
            
            if (virtualCamera != null)
            {
                composer = virtualCamera.GetCinemachineComponent<CinemachineComposer>();
                transposer = virtualCamera.GetCinemachineComponent<CinemachineTransposer>();
            }
            
            // Lock cursor to center of screen
            Cursor.lockState = CursorLockMode.Locked;
            Cursor.visible = false;
        }
        
        private void Start()
        {
            if (target == null)
            {
                PlayerController player = FindObjectOfType<PlayerController>();
                if (player != null)
                {
                    target = player.transform;
                    virtualCamera.Follow = target;
                    virtualCamera.LookAt = target;
                }
            }
            
            // Set initial camera position
            if (transposer != null)
            {
                transposer.m_FollowOffset = new Vector3(0, 2, -currentDistance);
            }
        }
        
        private void Update()
        {
            if (target == null) return;
            
            HandleMouseInput();
            HandleZoomInput();
            HandleCameraCollision();
        }
        
        private void HandleMouseInput()
        {
            float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity;
            float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity;
            
            currentRotationY += mouseX;
            currentRotationX -= mouseY;
            currentRotationX = Mathf.Clamp(currentRotationX, minVerticalAngle, maxVerticalAngle);
            
            if (composer != null)
            {
                composer.m_TrackedObjectOffset.x = currentRotationX;
                composer.m_TrackedObjectOffset.y = currentRotationY;
            }
        }
        
        private void HandleZoomInput()
        {
            float scroll = Input.GetAxis("Mouse ScrollWheel");
            if (Mathf.Abs(scroll) > 0.01f)
            {
                currentDistance -= scroll * zoomSpeed;
                currentDistance = Mathf.Clamp(currentDistance, minDistance, maxDistance);
                
                if (transposer != null)
                {
                    Vector3 offset = transposer.m_FollowOffset;
                    offset.z = -currentDistance;
                    transposer.m_FollowOffset = offset;
                }
            }
        }
        
        private void HandleCameraCollision()
        {
            if (transposer == null || target == null) return;
            
            Vector3 targetPosition = target.position;
            Vector3 cameraPosition = targetPosition + transposer.m_FollowOffset;
            
            // Check for obstacles between camera and target
            RaycastHit hit;
            Vector3 direction = (cameraPosition - targetPosition).normalized;
            float distance = Vector3.Distance(targetPosition, cameraPosition);
            
            if (Physics.SphereCast(targetPosition, collisionRadius, direction, out hit, distance, collisionLayers))
            {
                // Move camera closer to avoid collision
                float newDistance = hit.distance - collisionRadius;
                Vector3 newOffset = transposer.m_FollowOffset;
                newOffset.z = -newDistance;
                transposer.m_FollowOffset = newOffset;
            }
            else
            {
                // Gradually return to desired distance
                Vector3 currentOffset = transposer.m_FollowOffset;
                float targetZ = -currentDistance;
                currentOffset.z = Mathf.Lerp(currentOffset.z, targetZ, Time.deltaTime * 5f);
                transposer.m_FollowOffset = currentOffset;
            }
        }
        
        public void SetTarget(Transform newTarget)
        {
            target = newTarget;
            if (virtualCamera != null)
            {
                virtualCamera.Follow = target;
                virtualCamera.LookAt = target;
            }
        }
        
        public void SetMouseSensitivity(float sensitivity)
        {
            mouseSensitivity = sensitivity;
        }
        
        public void SetCameraDistance(float distance)
        {
            currentDistance = Mathf.Clamp(distance, minDistance, maxDistance);
            if (transposer != null)
            {
                Vector3 offset = transposer.m_FollowOffset;
                offset.z = -currentDistance;
                transposer.m_FollowOffset = offset;
            }
        }
        
        public void ShakeCamera(float intensity, float duration)
        {
            StartCoroutine(CameraShakeCoroutine(intensity, duration));
        }
        
        private System.Collections.IEnumerator CameraShakeCoroutine(float intensity, float duration)
        {
            Vector3 originalOffset = transposer.m_FollowOffset;
            float elapsed = 0f;
            
            while (elapsed < duration)
            {
                Vector3 shakeOffset = Random.insideUnitSphere * intensity;
                transposer.m_FollowOffset = originalOffset + shakeOffset;
                
                elapsed += Time.deltaTime;
                yield return null;
            }
            
            transposer.m_FollowOffset = originalOffset;
        }
        
        public void ToggleCursorLock()
        {
            if (Cursor.lockState == CursorLockMode.Locked)
            {
                Cursor.lockState = CursorLockMode.None;
                Cursor.visible = true;
            }
            else
            {
                Cursor.lockState = CursorLockMode.Locked;
                Cursor.visible = false;
            }
        }
        
        private void OnDrawGizmosSelected()
        {
            if (target != null)
            {
                Gizmos.color = Color.cyan;
                Gizmos.DrawWireSphere(target.position, collisionRadius);
                Gizmos.DrawLine(target.position, target.position + transposer.m_FollowOffset);
            }
        }
    }
}
