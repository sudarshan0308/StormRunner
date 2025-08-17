using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using System.IO;

namespace StormRunner
{
    public class AvatarCreationSystem : MonoBehaviour
    {
        [Header("UI Elements")]
        [SerializeField] private RawImage previewImage;
        [SerializeField] private Button takePhotoButton;
        [SerializeField] private Button retakeButton;
        [SerializeField] private Button confirmButton;
        [SerializeField] private Button backButton;
        [SerializeField] private GameObject cameraUI;
        [SerializeField] private GameObject avatarCustomizationUI;
        
        [Header("Camera Settings")]
        [SerializeField] private WebCamTexture webCamTexture;
        [SerializeField] private int preferredWidth = 640;
        [SerializeField] private int preferredHeight = 480;
        [SerializeField] private int preferredFPS = 30;
        
        [Header("Avatar Customization")]
        [SerializeField] private Slider skinToneSlider;
        [SerializeField] private Slider hairStyleSlider;
        [SerializeField] private Slider eyeColorSlider;
        [SerializeField] private Slider clothingStyleSlider;
        [SerializeField] private InputField playerNameInput;
        
        [Header("Avatar Preview")]
        [SerializeField] private GameObject avatarPreview;
        [SerializeField] private SkinnedMeshRenderer avatarRenderer;
        [SerializeField] private Material avatarMaterial;
        
        [Header("Audio")]
        [SerializeField] private AudioSource cameraShutterAudio;
        [SerializeField] private AudioClip cameraShutterSound;
        
        private Texture2D capturedPhoto;
        private bool isPhotoTaken = false;
        private string playerName = "";
        
        private void Start()
        {
            InitializeUI();
            SetupWebCam();
        }
        
        private void InitializeUI()
        {
            if (takePhotoButton != null)
                takePhotoButton.onClick.AddListener(TakePhoto);
            
            if (retakeButton != null)
                retakeButton.onClick.AddListener(RetakePhoto);
            
            if (confirmButton != null)
                confirmButton.confirmButton.onClick.AddListener(ConfirmAvatar);
            
            if (backButton != null)
                backButton.onClick.AddListener(GoBack);
            
            // Initially hide retake and confirm buttons
            if (retakeButton != null) retakeButton.gameObject.SetActive(false);
            if (confirmButton != null) confirmButton.gameObject.SetActive(false);
            if (avatarCustomizationUI != null) avatarCustomizationUI.SetActive(false);
        }
        
        private void SetupWebCam()
        {
            if (WebCamTexture.devices.Length == 0)
            {
                Debug.LogWarning("No webcam devices found!");
                return;
            }
            
            // Use front-facing camera if available
            WebCamDevice frontCamera = WebCamTexture.devices[0];
            for (int i = 0; i < WebCamTexture.devices.Length; i++)
            {
                if (WebCamTexture.devices[i].isFrontFacing)
                {
                    frontCamera = WebCamTexture.devices[i];
                    break;
                }
            }
            
            webCamTexture = new WebCamTexture(frontCamera.name, preferredWidth, preferredHeight, preferredFPS);
            
            if (previewImage != null)
            {
                previewImage.texture = webCamTexture;
            }
            
            webCamTexture.Play();
        }
        
        private void TakePhoto()
        {
            if (webCamTexture == null || !webCamTexture.isPlaying) return;
            
            // Play camera shutter sound
            if (cameraShutterAudio != null && cameraShutterSound != null)
            {
                cameraShutterAudio.PlayOneShot(cameraShutterSound);
            }
            
            // Capture the current frame
            StartCoroutine(CapturePhoto());
        }
        
        private IEnumerator CapturePhoto()
        {
            // Wait for the end of frame to ensure we get the current frame
            yield return new WaitForEndOfFrame();
            
            // Create a new texture from the webcam
            capturedPhoto = new Texture2D(webCamTexture.width, webCamTexture.height);
            capturedPhoto.SetPixels(webCamTexture.GetPixels());
            capturedPhoto.Apply();
            
            // Stop the webcam
            webCamTexture.Stop();
            
            // Show the captured photo
            if (previewImage != null)
            {
                previewImage.texture = capturedPhoto;
            }
            
            isPhotoTaken = true;
            
            // Show customization options
            ShowAvatarCustomization();
            
            // Update UI
            if (takePhotoButton != null) takePhotoButton.gameObject.SetActive(false);
            if (retakeButton != null) retakeButton.gameObject.SetActive(true);
            if (confirmButton != null) confirmButton.gameObject.SetActive(true);
        }
        
        private void RetakePhoto()
        {
            isPhotoTaken = false;
            
            // Clear the captured photo
            if (capturedPhoto != null)
            {
                Destroy(capturedPhoto);
                capturedPhoto = null;
            }
            
            // Restart webcam
            if (webCamTexture != null)
            {
                webCamTexture.Play();
                if (previewImage != null)
                {
                    previewImage.texture = webCamTexture;
                }
            }
            
            // Hide customization options
            if (avatarCustomizationUI != null) avatarCustomizationUI.SetActive(false);
            
            // Update UI
            if (takePhotoButton != null) takePhotoButton.gameObject.SetActive(true);
            if (retakeButton != null) retakeButton.gameObject.SetActive(false);
            if (confirmButton != null) confirmButton.gameObject.SetActive(false);
        }
        
        private void ShowAvatarCustomization()
        {
            if (avatarCustomizationUI != null)
            {
                avatarCustomizationUI.SetActive(true);
            }
            
            // Setup sliders
            if (skinToneSlider != null)
                skinToneSlider.onValueChanged.AddListener(OnSkinToneChanged);
            
            if (hairStyleSlider != null)
                hairStyleSlider.onValueChanged.AddListener(OnHairStyleChanged);
            
            if (eyeColorSlider != null)
                eyeColorSlider.onValueChanged.AddListener(OnEyeColorChanged);
            
            if (clothingStyleSlider != null)
                clothingStyleSlider.onValueChanged.AddListener(OnClothingStyleChanged);
            
            // Setup player name input
            if (playerNameInput != null)
            {
                playerNameInput.onEndEdit.AddListener(OnPlayerNameChanged);
                playerNameInput.text = "Player";
            }
            
            // Generate initial avatar
            GenerateAvatar();
        }
        
        private void GenerateAvatar()
        {
            if (avatarRenderer == null || avatarMaterial == null) return;
            
            // Apply the captured photo as the base texture
            if (capturedPhoto != null)
            {
                avatarMaterial.mainTexture = capturedPhoto;
            }
            
            // Apply customization values
            ApplyCustomizations();
        }
        
        private void ApplyCustomizations()
        {
            if (avatarRenderer == null || avatarMaterial == null) return;
            
            // Apply skin tone
            if (skinToneSlider != null)
            {
                Color skinTone = Color.Lerp(Color.white, new Color(0.8f, 0.6f, 0.5f), skinToneSlider.value);
                avatarMaterial.SetColor("_SkinTone", skinTone);
            }
            
            // Apply hair style (this would typically involve different hair meshes)
            if (hairStyleSlider != null)
            {
                // Hair style logic would go here
            }
            
            // Apply eye color
            if (eyeColorSlider != null)
            {
                Color eyeColor = Color.Lerp(Color.blue, Color.brown, eyeColorSlider.value);
                avatarMaterial.SetColor("_EyeColor", eyeColor);
            }
            
            // Apply clothing style
            if (clothingStyleSlider != null)
            {
                // Clothing style logic would go here
            }
        }
        
        private void OnSkinToneChanged(float value)
        {
            ApplyCustomizations();
        }
        
        private void OnHairStyleChanged(float value)
        {
            ApplyCustomizations();
        }
        
        private void OnEyeColorChanged(float value)
        {
            ApplyCustomizations();
        }
        
        private void OnClothingStyleChanged(float value)
        {
            ApplyCustomizations();
        }
        
        private void OnPlayerNameChanged(string name)
        {
            playerName = name;
        }
        
        private void ConfirmAvatar()
        {
            if (capturedPhoto == null) return;
            
            // Save the avatar texture
            string avatarPath = SaveAvatarTexture();
            
            // Update player data
            if (GameManager.Instance != null)
            {
                GameManager.Instance.CurrentPlayerData.HasAvatar = true;
                GameManager.Instance.CurrentPlayerData.avatarTexturePath = avatarPath;
                GameManager.Instance.CurrentPlayerData.playerName = playerName;
            }
            
            // Start the game
            if (GameManager.Instance != null)
            {
                GameManager.Instance.LoadGameScene();
            }
        }
        
        private string SaveAvatarTexture()
        {
            if (capturedPhoto == null) return "";
            
            // Convert to PNG
            byte[] pngData = capturedPhoto.EncodeToPNG();
            
            // Save to persistent data path
            string fileName = "avatar_" + System.DateTime.Now.Ticks + ".png";
            string filePath = Path.Combine(Application.persistentDataPath, fileName);
            
            File.WriteAllBytes(filePath, pngData);
            
            Debug.Log("Avatar saved to: " + filePath);
            return filePath;
        }
        
        private void GoBack()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.LoadMainMenu();
            }
        }
        
        private void OnDestroy()
        {
            if (webCamTexture != null)
            {
                webCamTexture.Stop();
            }
            
            if (capturedPhoto != null)
            {
                Destroy(capturedPhoto);
            }
        }
        
        private void OnApplicationPause(bool pauseStatus)
        {
            if (pauseStatus && webCamTexture != null)
            {
                webCamTexture.Pause();
            }
            else if (!pauseStatus && webCamTexture != null && !isPhotoTaken)
            {
                webCamTexture.Play();
            }
        }
        
        private void OnApplicationFocus(bool hasFocus)
        {
            if (!hasFocus && webCamTexture != null)
            {
                webCamTexture.Pause();
            }
            else if (hasFocus && webCamTexture != null && !isPhotoTaken)
            {
                webCamTexture.Play();
            }
        }
    }
}
