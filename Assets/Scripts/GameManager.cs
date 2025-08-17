using UnityEngine;
using UnityEngine.SceneManagement;
using System.Collections;

namespace StormRunner
{
    public class GameManager : MonoBehaviour
    {
        [Header("Game Settings")]
        public static GameManager Instance { get; private set; }
        
        [SerializeField] private string mainMenuScene = "MainMenu";
        [SerializeField] private string gameScene = "GameScene";
        [SerializeField] private string avatarCreationScene = "AvatarCreation";
        
        [Header("Game State")]
        public GameState CurrentGameState { get; private set; }
        public PlayerData CurrentPlayerData { get; private set; }
        
        [Header("Audio")]
        [SerializeField] private AudioSource musicSource;
        [SerializeField] private AudioSource sfxSource;
        
        private void Awake()
        {
            if (Instance == null)
            {
                Instance = this;
                DontDestroyOnLoad(gameObject);
                InitializeGame();
            }
            else
            {
                Destroy(gameObject);
            }
        }
        
        private void InitializeGame()
        {
            CurrentGameState = GameState.MainMenu;
            LoadPlayerData();
            SetupAudio();
        }
        
        private void LoadPlayerData()
        {
            CurrentPlayerData = new PlayerData();
            string savedData = PlayerPrefs.GetString("PlayerData", "");
            if (!string.IsNullOrEmpty(savedData))
            {
                CurrentPlayerData = JsonUtility.FromJson<PlayerData>(savedData);
            }
        }
        
        private void SavePlayerData()
        {
            if (CurrentPlayerData != null)
            {
                string jsonData = JsonUtility.ToJson(CurrentPlayerData);
                PlayerPrefs.SetString("PlayerData", jsonData);
                PlayerPrefs.Save();
            }
        }
        
        private void SetupAudio()
        {
            if (musicSource != null)
            {
                musicSource.volume = PlayerPrefs.GetFloat("MusicVolume", 0.7f);
            }
            if (sfxSource != null)
            {
                sfxSource.volume = PlayerPrefs.GetFloat("SFXVolume", 1.0f);
            }
        }
        
        public void StartNewGame()
        {
            if (CurrentPlayerData.HasAvatar)
            {
                LoadGameScene();
            }
            else
            {
                LoadAvatarCreation();
            }
        }
        
        public void LoadMainMenu()
        {
            CurrentGameState = GameState.MainMenu;
            SceneManager.LoadScene(mainMenuScene);
        }
        
        public void LoadAvatarCreation()
        {
            CurrentGameState = GameState.AvatarCreation;
            SceneManager.LoadScene(avatarCreationScene);
        }
        
        public void LoadGameScene()
        {
            CurrentGameState = GameState.Playing;
            SceneManager.LoadScene(gameScene);
        }
        
        public void PauseGame()
        {
            if (CurrentGameState == GameState.Playing)
            {
                CurrentGameState = GameState.Paused;
                Time.timeScale = 0f;
            }
        }
        
        public void ResumeGame()
        {
            if (CurrentGameState == GameState.Paused)
            {
                CurrentGameState = GameState.Playing;
                Time.timeScale = 1f;
            }
        }
        
        public void QuitGame()
        {
            SavePlayerData();
            #if UNITY_EDITOR
                UnityEditor.EditorApplication.isPlaying = false;
            #else
                Application.Quit();
            #endif
        }
        
        public void SetMusicVolume(float volume)
        {
            if (musicSource != null)
            {
                musicSource.volume = volume;
                PlayerPrefs.SetFloat("MusicVolume", volume);
                PlayerPrefs.Save();
            }
        }
        
        public void SetSFXVolume(float volume)
        {
            if (sfxSource != null)
            {
                sfxSource.volume = volume;
                PlayerPrefs.SetFloat("SFXVolume", volume);
                PlayerPrefs.Save();
            }
        }
        
        private void OnApplicationPause(bool pauseStatus)
        {
            if (pauseStatus && CurrentGameState == GameState.Playing)
            {
                PauseGame();
            }
        }
        
        private void OnApplicationFocus(bool hasFocus)
        {
            if (!hasFocus && CurrentGameState == GameState.Playing)
            {
                PauseGame();
            }
        }
    }
    
    public enum GameState
    {
        MainMenu,
        AvatarCreation,
        Playing,
        Paused,
        GameOver
    }
    
    [System.Serializable]
    public class PlayerData
    {
        public string playerName = "Player";
        public bool HasAvatar = false;
        public string avatarTexturePath = "";
        public float gameProgress = 0f;
        public int totalScore = 0;
        public int highScore = 0;
        public float playTime = 0f;
    }
}
