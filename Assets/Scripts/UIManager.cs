using UnityEngine;
using UnityEngine.UI;
using TMPro;

namespace StormRunner
{
    public class UIManager : MonoBehaviour
    {
        [Header("HUD Elements")]
        [SerializeField] private GameObject hudPanel;
        [SerializeField] private TextMeshProUGUI playerNameText;
        [SerializeField] private TextMeshProUGUI weatherStatusText;
        [SerializeField] private Slider healthBar;
        [SerializeField] private TextMeshProUGUI interactionPrompt;
        
        [Header("Pause Menu")]
        [SerializeField] private GameObject pauseMenuPanel;
        [SerializeField] private Button resumeButton;
        [SerializeField] private Button settingsButton;
        [SerializeField] private Button mainMenuButton;
        
        [Header("Settings Panel")]
        [SerializeField] private GameObject settingsPanel;
        [SerializeField] private Slider musicVolumeSlider;
        [SerializeField] private Slider sfxVolumeSlider;
        [SerializeField] private Slider mouseSensitivitySlider;
        [SerializeField] private Button settingsBackButton;
        
        private bool isPaused = false;
        private WeatherSystem weatherSystem;
        private PlayerController playerController;
        
        private void Start()
        {
            InitializeUI();
            FindGameComponents();
            SetupEventListeners();
        }
        
        private void InitializeUI()
        {
            if (pauseMenuPanel != null) pauseMenuPanel.SetActive(false);
            if (settingsPanel != null) settingsPanel.SetActive(false);
            if (hudPanel != null) hudPanel.SetActive(true);
            
            // Initialize interaction prompt as hidden
            if (interactionPrompt != null) interactionPrompt.gameObject.SetActive(false);
        }
        
        private void FindGameComponents()
        {
            weatherSystem = FindObjectOfType<WeatherSystem>();
            playerController = FindObjectOfType<PlayerController>();
            
            // Update player name if available
            if (playerNameText != null && GameManager.Instance != null)
            {
                playerNameText.text = GameManager.Instance.CurrentPlayerData.playerName;
            }
        }
        
        private void SetupEventListeners()
        {
            if (resumeButton != null)
                resumeButton.onClick.AddListener(ResumeGame);
            
            if (settingsButton != null)
                settingsButton.onClick.AddListener(OpenSettings);
            
            if (mainMenuButton != null)
                mainMenuButton.onClick.AddListener(ReturnToMainMenu);
            
            if (settingsBackButton != null)
                settingsBackButton.onClick.AddListener(CloseSettings);
            
            if (musicVolumeSlider != null)
                musicVolumeSlider.onValueChanged.AddListener(OnMusicVolumeChanged);
            
            if (sfxVolumeSlider != null)
                sfxVolumeSlider.onValueChanged.AddListener(OnSFXVolumeChanged);
            
            if (mouseSensitivitySlider != null)
                mouseSensitivitySlider.onValueChanged.AddListener(OnMouseSensitivityChanged);
        }
        
        private void Update()
        {
            HandlePauseInput();
            UpdateHUD();
        }
        
        private void HandlePauseInput()
        {
            if (Input.GetKeyDown(KeyCode.Escape) || Input.GetKeyDown(KeyCode.Tab))
            {
                if (settingsPanel != null && settingsPanel.activeSelf)
                {
                    CloseSettings();
                }
                else if (isPaused)
                {
                    ResumeGame();
                }
                else
                {
                    PauseGame();
                }
            }
        }
        
        private void UpdateHUD()
        {
            // Update weather status
            if (weatherStatusText != null && weatherSystem != null)
            {
                weatherStatusText.text = "Weather: " + weatherSystem.GetCurrentWeather().ToString();
            }
            
            // Update health bar (placeholder - you can implement actual health system)
            if (healthBar != null)
            {
                healthBar.value = 1f; // Full health for now
            }
        }
        
        public void PauseGame()
        {
            isPaused = true;
            Time.timeScale = 0f;
            
            if (pauseMenuPanel != null) pauseMenuPanel.SetActive(true);
            if (hudPanel != null) hudPanel.SetActive(false);
            
            // Unlock cursor for menu navigation
            Cursor.lockState = CursorLockMode.None;
            Cursor.visible = true;
            
            if (GameManager.Instance != null)
                GameManager.Instance.PauseGame();
        }
        
        public void ResumeGame()
        {
            isPaused = false;
            Time.timeScale = 1f;
            
            if (pauseMenuPanel != null) pauseMenuPanel.SetActive(false);
            if (hudPanel != null) hudPanel.SetActive(true);
            
            // Lock cursor back for gameplay
            Cursor.lockState = CursorLockMode.Locked;
            Cursor.visible = false;
            
            if (GameManager.Instance != null)
                GameManager.Instance.ResumeGame();
        }
        
        private void OpenSettings()
        {
            if (settingsPanel != null) settingsPanel.SetActive(true);
            if (pauseMenuPanel != null) pauseMenuPanel.SetActive(false);
            
            // Load current settings
            if (musicVolumeSlider != null)
                musicVolumeSlider.value = PlayerPrefs.GetFloat("MusicVolume", 0.7f);
            
            if (sfxVolumeSlider != null)
                sfxVolumeSlider.value = PlayerPrefs.GetFloat("SFXVolume", 1.0f);
            
            if (mouseSensitivitySlider != null)
                mouseSensitivitySlider.value = PlayerPrefs.GetFloat("MouseSensitivity", 2.0f);
        }
        
        private void CloseSettings()
        {
            if (settingsPanel != null) settingsPanel.SetActive(false);
            if (pauseMenuPanel != null) pauseMenuPanel.SetActive(true);
        }
        
        private void ReturnToMainMenu()
        {
            Time.timeScale = 1f;
            if (GameManager.Instance != null)
            {
                GameManager.Instance.LoadMainMenu();
            }
        }
        
        private void OnMusicVolumeChanged(float value)
        {
            PlayerPrefs.SetFloat("MusicVolume", value);
            PlayerPrefs.Save();
            
            AudioManager audioManager = FindObjectOfType<AudioManager>();
            if (audioManager != null)
            {
                audioManager.SetMusicVolume(value);
            }
        }
        
        private void OnSFXVolumeChanged(float value)
        {
            PlayerPrefs.SetFloat("SFXVolume", value);
            PlayerPrefs.Save();
            
            AudioManager audioManager = FindObjectOfType<AudioManager>();
            if (audioManager != null)
            {
                audioManager.SetSFXVolume(value);
            }
        }
        
        private void OnMouseSensitivityChanged(float value)
        {
            PlayerPrefs.SetFloat("MouseSensitivity", value);
            PlayerPrefs.Save();
            
            CameraController cameraController = FindObjectOfType<CameraController>();
            if (cameraController != null)
            {
                cameraController.SetMouseSensitivity(value);
            }
        }
        
        public void ShowInteractionPrompt(string text)
        {
            if (interactionPrompt != null)
            {
                interactionPrompt.text = text;
                interactionPrompt.gameObject.SetActive(true);
            }
        }
        
        public void HideInteractionPrompt()
        {
            if (interactionPrompt != null)
            {
                interactionPrompt.gameObject.SetActive(false);
            }
        }
        
        public void UpdatePlayerName(string name)
        {
            if (playerNameText != null)
            {
                playerNameText.text = name;
            }
        }
    }
}