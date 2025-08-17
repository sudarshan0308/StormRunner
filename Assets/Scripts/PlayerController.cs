using UnityEngine;
using UnityEngine.InputSystem;

namespace StormRunner
{
    [RequireComponent(typeof(CharacterController))]
    [RequireComponent(typeof(Animator))]
    public class PlayerController : MonoBehaviour
    {
        [Header("Movement Settings")]
        [SerializeField] private float walkSpeed = 6f;
        [SerializeField] private float runSpeed = 12f;
        [SerializeField] private float jumpHeight = 2f;
        [SerializeField] private float gravity = -9.81f;
        [SerializeField] private float groundCheckDistance = 0.4f;
        [SerializeField] private LayerMask groundMask = 1;
        
        [Header("Animation")]
        [SerializeField] private Animator animator;
        [SerializeField] private Transform groundCheck;
        
        [Header("Audio")]
        [SerializeField] private AudioSource footstepsAudio;
        [SerializeField] private AudioClip[] footstepSounds;
        [SerializeField] private AudioClip jumpSound;
        [SerializeField] private AudioClip landSound;
        
        private CharacterController controller;
        private Vector3 velocity;
        private bool isGrounded;
        private bool isRunning;
        private float currentSpeed;
        
        // Input values
        private Vector2 moveInput;
        private bool jumpPressed;
        private bool runPressed;
        
        // Animation parameters
        private readonly int IsWalkingHash = Animator.StringToHash("IsWalking");
        private readonly int IsRunningHash = Animator.StringToHash("IsRunning");
        private readonly int IsJumpingHash = Animator.StringToHash("IsJumping");
        private readonly int IsGroundedHash = Animator.StringToHash("IsGrounded");
        
        private void Awake()
        {
            controller = GetComponent<CharacterController>();
            if (animator == null)
                animator = GetComponent<Animator>();
            
            if (groundCheck == null)
            {
                GameObject groundCheckObj = new GameObject("GroundCheck");
                groundCheckObj.transform.SetParent(transform);
                groundCheckObj.transform.localPosition = Vector3.down * 0.9f;
                groundCheck = groundCheckObj.transform;
            }
        }
        
        private void Start()
        {
            currentSpeed = walkSpeed;
        }
        
        private void Update()
        {
            HandleGroundCheck();
            HandleMovement();
            HandleJump();
            HandleGravity();
            UpdateAnimations();
            HandleFootsteps();
        }
        
        private void HandleGroundCheck()
        {
            isGrounded = Physics.CheckSphere(groundCheck.position, groundCheckDistance, groundMask);
            
            if (isGrounded && velocity.y < 0)
            {
                velocity.y = -2f;
            }
        }
        
        private void HandleMovement()
        {
            Vector3 move = transform.right * moveInput.x + transform.forward * moveInput.y;
            
            // Update speed based on run state
            currentSpeed = runPressed ? runSpeed : walkSpeed;
            
            controller.Move(move * currentSpeed * Time.deltaTime);
        }
        
        private void HandleJump()
        {
            if (jumpPressed && isGrounded)
            {
                velocity.y = Mathf.Sqrt(jumpHeight * -2f * gravity);
                
                if (jumpSound != null && footstepsAudio != null)
                {
                    footstepsAudio.PlayOneShot(jumpSound);
                }
                
                jumpPressed = false;
            }
        }
        
        private void HandleGravity()
        {
            velocity.y += gravity * Time.deltaTime;
            controller.Move(velocity * Time.deltaTime);
        }
        
        private void UpdateAnimations()
        {
            bool isMoving = moveInput.magnitude > 0.1f;
            
            animator.SetBool(IsWalkingHash, isMoving && !isRunning);
            animator.SetBool(IsRunningHash, isMoving && isRunning);
            animator.SetBool(IsJumpingHash, !isGrounded);
            animator.SetBool(IsGroundedHash, isGrounded);
        }
        
        private void HandleFootsteps()
        {
            if (footstepsAudio != null && footstepSounds.Length > 0 && isGrounded && moveInput.magnitude > 0.1f)
            {
                if (!footstepsAudio.isPlaying)
                {
                    AudioClip randomFootstep = footstepSounds[Random.Range(0, footstepSounds.Length)];
                    footstepsAudio.clip = randomFootstep;
                    footstepsAudio.pitch = Random.Range(0.9f, 1.1f);
                    footstepsAudio.Play();
                }
            }
        }
        
        // Input System callbacks
        public void OnMove(InputValue value)
        {
            moveInput = value.Get<Vector2>();
        }
        
        public void OnJump(InputValue value)
        {
            jumpPressed = value.isPressed;
        }
        
        public void OnRun(InputValue value)
        {
            runPressed = value.isPressed;
            isRunning = runPressed;
        }
        
        public void OnInteract(InputValue value)
        {
            if (value.isPressed)
            {
                TryInteract();
            }
        }
        
        private void TryInteract()
        {
            // Raycast to find interactable objects
            RaycastHit hit;
            if (Physics.Raycast(transform.position + Vector3.up, transform.forward, out hit, 3f))
            {
                IInteractable interactable = hit.collider.GetComponent<IInteractable>();
                if (interactable != null)
                {
                    interactable.Interact(this);
                }
            }
        }
        
        public void SetAvatarTexture(Texture2D texture)
        {
            // Apply the avatar texture to the player model
            SkinnedMeshRenderer renderer = GetComponentInChildren<SkinnedMeshRenderer>();
            if (renderer != null)
            {
                renderer.material.mainTexture = texture;
            }
        }
        
        public void SetPlayerName(string name)
        {
            GameManager.Instance.CurrentPlayerData.playerName = name;
        }
        
        private void OnDrawGizmosSelected()
        {
            if (groundCheck != null)
            {
                Gizmos.color = Color.yellow;
                Gizmos.DrawWireSphere(groundCheck.position, groundCheckDistance);
            }
        }
    }
    
    public interface IInteractable
    {
        void Interact(PlayerController player);
    }
}
