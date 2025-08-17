using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using TMPro;

namespace StormRunner
{
    public class MainMenuUI : MonoBehaviour
    {
        [Header("Main Menu Panels")]
        [SerializeField] private GameObject mainMenuPanel;
        [SerializeField] private GameObject settingsPanel;
        [SerializeField] private GameObject creditsPanel;
        [SerializeField] private GameObject quitConfirmPanel;
        
        [Header("Main Menu Buttons")]
        [SerializeField] private Button playButton;
        [SerializeField] private Button settingsButton;
        [SerializeField] private Button creditsButton;
        [SerializeField] private Button quitButton;
        
        [Header("Settings Panel")]
        [SerializeField] private Slider musicVolumeSlider;
        [SerializeField] private Slider sfxVolumeSlider;
        [SerializeField] private Slider mouseSensitivitySlider;
        [SerializeField] private Toggle fullscreenToggle;
        [SerializeField] private Button settingsBackButton;
        
        [Header("Credits Panel")]
        [SerializeField] private Button creditsBackButton;
        
        [Header("Quit Confirm Panel")]
        [SerializeField] private Button quitConfirmButton;
        [SerializeField] private Button quitCancelButton;
        
        [Header("Audio")]
        [SerializeField] private AudioSource menuAudio;
        [SerializeField] private AudioClip buttonClickSound;
        [SerializeField] private AudioClip menuMusic;
        
        [Header("Animation")]
        [SerializeField] private Animator menuAnimator;
        [SerializeField] private float buttonHoverScale = 1.1f;
        [SerializeField] private float buttonClickScale = 0.95f;
        
        private void Start()
        {
            InitializeUI();
            SetupAudio();
            ShowMainMenu();
        }
        
        private void InitializeUI()
        {
            // Main menu buttons
            if (playButton != null)
                playButton.onClick.AddListener(OnPlayButtonClicked);
            
            if (settingsButton != null)
                settingsButton.onClick.AddListener(OnSettingsButtonClicked);
            
            if (creditsButton != null)
                creditsButton.onClick.AddListener(OnCreditsButtonClicked);
            
            if (quitButton != null)
                quitButton.onClick.AddListener(OnQuitButtonClicked);
            
            // Settings panel
            if (musicVolumeSlider != null)
                musicVolumeSlider.onValueChanged.AddListener(OnMusicVolumeChanged);
            
            if (sfxVolumeSlider != null)
                sfxVolumeSlider.onValueChanged.AddListener(OnSFXVolumeChanged);
            
            if (mouseSensitivitySlider != null)
                mouseSensitivitySlider.onValueChanged.AddListener(OnMouseSensitivityChanged);
            
            if (fullscreenToggle != null)
                fullscreenToggle.onValueChanged.AddListener(OnFullscreenChanged);
            
            if (settingsBackButton != null)
                settingsBackButton.onClick.AddListener(OnSettingsBackClicked);
            
            // Credits panel
            if (creditsBackButton != null)
                creditsBackButton.onClick.AddListener(OnCreditsBackClicked);
            
            // Quit confirm panel
            if (quitConfirmButton != null)
                quitConfirmButton.onClick.AddListener(OnQuitConfirmClicked);
            
            if (quitCancelButton != null)
                quitCancelButton.onClick.AddListener(OnQuitCancelClicked);
            
            // Setup initial values
            SetupInitialValues();
            
            // Add hover effects to all buttons
            AddButtonHoverEffects();
        }
        
        private void SetupAudio()
        {
            if (menuAudio != null && menuMusic != null)
            {
                menuAudio.clip = menuMusic;
                menuAudio.loop = true;
                menuAudio.Play();
            }
        }
        
        private void SetupInitialValues()
        {
            // Load saved settings
            if (musicVolumeSlider != null)
                musicVolumeSlider.value = PlayerPrefs.GetFloat("MusicVolume", 0.7f);
            
            if (sfxVolumeSlider != null)
                sfxVolumeSlider.value = PlayerPrefs.GetFloat("SFXVolume", 1.0f);
            
            if (mouseSensitivitySlider != null)
                mouseSensitivitySlider.value = PlayerPrefs.GetFloat("MouseSensitivity", 2.0f);
            
            if (fullscreenToggle != null)
                fullscreenToggle.isOn = Screen.fullScreen;
        }
        
        private void AddButtonHoverEffects()
        {
            Button[] allButtons = GetComponentsInChildren<Button>();
            foreach (Button button in allButtons)
            {
                // Add hover effect
                EventTrigger trigger = button.gameObject.GetComponent<EventTrigger>();
                if (trigger == null)
                    trigger = button.gameObject.AddComponent<EventTrigger>();
                
                // Pointer Enter
                EventTrigger.Entry enterEntry = new EventTrigger.Entry();
                enterEntry.eventID = EventTriggerType.PointerEnter;
                enterEntry.callback.AddListener((data) => { OnButtonHover(button.transform, true); });
                trigger.triggers.Add(enterEntry);
                
                // Pointer Exit
                EventTrigger.Entry exitEntry = new EventTrigger.Entry();
                exitEntry.eventID = EventTriggerType.PointerExit;
                exitEntry.callback.AddListener((data) => { OnButtonHover(button.transform, false); });
                trigger.triggers.Add(exitEntry);
                
                // Pointer Click
                EventTrigger.Entry clickEntry = new EventTrigger.Entry();
                clickEntry.eventID = EventTriggerType.PointerClick;
                clickEntry.callback.AddListener((data) => { OnButtonClick(button.transform); });
                trigger.triggers.Add(clickEntry);
            }
        }
        
        private void OnButtonHover(Transform buttonTransform, bool isHovering)
        {
            if (buttonTransform != null)
            {
                float targetScale = isHovering ? buttonHoverScale : 1f;
                buttonTransform.localScale = Vector3.one * targetScale;
            }
        }
        
        private void OnButtonClick(Transform buttonTransform)
        {
            if (buttonTransform != null)
            {
                StartCoroutine(ButtonClickAnimation(buttonTransform));
            }
            
            // Play click sound
            if (menuAudio != null && buttonClickSound != null)
            {
                menuAudio.PlayOneShot(buttonClickSound);
            }
        }
        
        private System.Collections.IEnumerator ButtonClickAnimation(Transform buttonTransform)
        {
            Vector3 originalScale = buttonTransform.localScale;
            buttonTransform.localScale = originalScale * buttonClickScale;
            
            yield return new WaitForSeconds(0.1f);
            
            buttonTransform.localScale = originalScale;
        }
        
        private void ShowMainMenu()
        {
            mainMenuPanel.SetActive(true);
            settingsPanel.SetActive(false);
            creditsPanel.SetActive(false);
            quitConfirmPanel.SetActive(false);
            
            if (menuAnimator != null)
                menuAnimator.SetTrigger("ShowMainMenu");
        }
        
        private void OnPlayButtonClicked()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.StartNewGame();
            }
        }
        
        private void OnSettingsButtonClicked()
        {
            mainMenuPanel.SetActive(false);
            settingsPanel.SetActive(true);
            
            if (menuAnimator != null)
                menuAnimator.SetTrigger("ShowSettings");
        }
        
        private void OnCreditsButtonClicked()
        {
            mainMenuPanel.SetActive(false);
            creditsPanel.SetActive(true);
            
            if (menuAnimator != null)
                menuAnimator.SetTrigger("ShowCredits");
        }
        
        private void OnQuitButtonClicked()
        {
            quitConfirmPanel.SetActive(true);
        }
        
        private void OnSettingsBackClicked()
        {
            settingsPanel.SetActive(false);
            ShowMainMenu();
        }
        
        private void OnCreditsBackClicked()
        {
            creditsPanel.SetActive(false);
            ShowMainMenu();
        }
        
        private void OnQuitConfirmClicked()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.QuitGame();
            }
            else
            {
                #if UNITY_EDITOR
                    UnityEditor.EditorApplication.isPlaying = false;
                #else
                    Application.Quit();
                #endif
            }
        }
        
        private void OnQuitCancelClicked()
        {
            quitConfirmPanel.SetActive(false);
        }
        
        private void OnMusicVolumeChanged(float value)
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.SetMusicVolume(value);
            }
            else
            {
                PlayerPrefs.SetFloat("MusicVolume", value);
                PlayerPrefs.Save();
            }
        }
        
        private void OnSFXVolumeChanged(float value)
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.SetSFXVolume(value);
            }
            else
            {
                PlayerPrefs.SetFloat("SFXVolume", value);
                PlayerPrefs.Save();
            }
        }
        
        private void OnMouseSensitivityChanged(float value)
        {
            PlayerPrefs.SetFloat("MouseSensitivity", value);
            PlayerPrefs.Save();
        }
        
        private void OnFullscreenChanged(bool isFullscreen)
        {
            Screen.fullScreen = isFullscreen;
        }
        
        private void Update()
        {
            // Handle escape key for back navigation
            if (Input.GetKeyDown(KeyCode.Escape))
            {
                if (quitConfirmPanel.activeSelf)
                {
                    OnQuitCancelClicked();
                }
                else if (settingsPanel.activeSelf)
                {
                    OnSettingsBackClicked();
                }
                else if (creditsPanel.activeSelf)
                {
                    OnCreditsBackClicked();
                }
                else if (mainMenuPanel.activeSelf)
                {
                    OnQuitButtonClicked();
                }
            }
        }
        
        public void SetMenuMusicVolume(float volume)
        {
            if (menuAudio != null)
            {
                menuAudio.volume = volume;
            }
        }
        
        public void PlayButtonSound()
        {
            if (menuAudio != null && buttonClickSound != null)
            {
                menuAudio.PlayOneShot(buttonClickSound);
            }
        }
    }
}
