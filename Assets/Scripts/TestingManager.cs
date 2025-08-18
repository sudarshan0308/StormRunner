using UnityEngine;
using System.Collections;

namespace StormRunner
{
    public class TestingManager : MonoBehaviour
    {
        [Header("Testing Settings")]
        [SerializeField] private bool enableTestingMode = false;
        [SerializeField] private KeyCode testingToggleKey = KeyCode.F1;
        [SerializeField] private GameObject testingUI;
        
        [Header("Test Objects")]
        [SerializeField] private GameObject testPlayer;
        [SerializeField] private Transform[] testSpawnPoints;
        
        private bool testingUIActive = false;
        private PlayerController playerController;
        private WeatherSystem weatherSystem;
        private AudioManager audioManager;
        
        private void Start()
        {
            if (testingUI != null)
                testingUI.SetActive(false);
            
            FindTestComponents();
        }
        
        private void FindTestComponents()
        {
            playerController = FindObjectOfType<PlayerController>();
            weatherSystem = FindObjectOfType<WeatherSystem>();
            audioManager = FindObjectOfType<AudioManager>();
        }
        
        private void Update()
        {
            if (enableTestingMode)
            {
                HandleTestingInput();
            }
        }
        
        private void HandleTestingInput()
        {
            // Toggle testing UI
            if (Input.GetKeyDown(testingToggleKey))
            {
                ToggleTestingUI();
            }
            
            // Weather testing
            if (Input.GetKeyDown(KeyCode.F2))
            {
                TestWeatherCycle();
            }
            
            // Audio testing
            if (Input.GetKeyDown(KeyCode.F3))
            {
                TestAudioSystems();
            }
            
            // Player testing
            if (Input.GetKeyDown(KeyCode.F4))
            {
                TestPlayerSystems();
            }
            
            // Performance testing
            if (Input.GetKeyDown(KeyCode.F5))
            {
                TestPerformance();
            }
        }
        
        private void ToggleTestingUI()
        {
            testingUIActive = !testingUIActive;
            if (testingUI != null)
            {
                testingUI.SetActive(testingUIActive);
            }
            
            Debug.Log($"Testing UI: {(testingUIActive ? "Enabled" : "Disabled")}");
        }
        
        private void TestWeatherCycle()
        {
            if (weatherSystem != null)
            {
                WeatherState[] weatherStates = { WeatherState.Clear, WeatherState.LightRain, WeatherState.HeavyRain, WeatherState.Storm };
                WeatherState randomWeather = weatherStates[Random.Range(0, weatherStates.Length)];
                weatherSystem.SetWeather(randomWeather);
                Debug.Log($"Testing: Set weather to {randomWeather}");
            }
        }
        
        private void TestAudioSystems()
        {
            if (audioManager != null)
            {
                audioManager.PlayFootstep();
                audioManager.PlayJump();
                audioManager.PlayInteraction();
                Debug.Log("Testing: Played test audio clips");
            }
        }
        
        private void TestPlayerSystems()
        {
            if (playerController != null && testSpawnPoints.Length > 0)
            {
                Transform randomSpawn = testSpawnPoints[Random.Range(0, testSpawnPoints.Length)];
                playerController.transform.position = randomSpawn.position;
                playerController.transform.rotation = randomSpawn.rotation;
                Debug.Log($"Testing: Teleported player to {randomSpawn.name}");
            }
        }
        
        private void TestPerformance()
        {
            StartCoroutine(PerformanceTest());
        }
        
        private IEnumerator PerformanceTest()
        {
            Debug.Log("Testing: Starting performance test...");
            
            float startTime = Time.time;
            int frameCount = 0;
            float totalFrameTime = 0f;
            
            while (Time.time - startTime < 5f) // Test for 5 seconds
            {
                totalFrameTime += Time.unscaledDeltaTime;
                frameCount++;
                yield return null;
            }
            
            float averageFPS = frameCount / (Time.time - startTime);
            float averageFrameTime = (totalFrameTime / frameCount) * 1000f; // Convert to milliseconds
            
            Debug.Log($"Performance Test Results:");
            Debug.Log($"Average FPS: {averageFPS:F2}");
            Debug.Log($"Average Frame Time: {averageFrameTime:F2}ms");
            Debug.Log($"Total Frames: {frameCount}");
        }
        
        public void RunFullSystemTest()
        {
            StartCoroutine(FullSystemTestCoroutine());
        }
        
        private IEnumerator FullSystemTestCoroutine()
        {
            Debug.Log("Starting full system test...");
            
            // Test Game Manager
            if (GameManager.Instance != null)
            {
                Debug.Log("✓ GameManager found and initialized");
            }
            else
            {
                Debug.LogError("✗ GameManager not found!");
            }
            
            yield return new WaitForSeconds(0.5f);
            
            // Test Player Controller
            if (playerController != null)
            {
                Debug.Log("✓ PlayerController found and initialized");
            }
            else
            {
                Debug.LogError("✗ PlayerController not found!");
            }
            
            yield return new WaitForSeconds(0.5f);
            
            // Test Weather System
            if (weatherSystem != null)
            {
                Debug.Log("✓ WeatherSystem found and initialized");
                TestWeatherCycle();
            }
            else
            {
                Debug.LogError("✗ WeatherSystem not found!");
            }
            
            yield return new WaitForSeconds(0.5f);
            
            // Test Audio Manager
            if (audioManager != null)
            {
                Debug.Log("✓ AudioManager found and initialized");
                TestAudioSystems();
            }
            else
            {
                Debug.LogError("✗ AudioManager not found!");
            }
            
            yield return new WaitForSeconds(0.5f);
            
            Debug.Log("Full system test completed!");
        }
        
        private void OnGUI()
        {
            if (enableTestingMode && testingUIActive)
            {
                GUILayout.BeginArea(new Rect(Screen.width - 250, 10, 240, 300));
                GUILayout.BeginVertical("box");
                
                GUILayout.Label("StormRunner Testing", GUI.skin.box);
                
                if (GUILayout.Button("Test Weather Cycle"))
                {
                    TestWeatherCycle();
                }
                
                if (GUILayout.Button("Test Audio Systems"))
                {
                    TestAudioSystems();
                }
                
                if (GUILayout.Button("Test Player Systems"))
                {
                    TestPlayerSystems();
                }
                
                if (GUILayout.Button("Test Performance"))
                {
                    TestPerformance();
                }
                
                if (GUILayout.Button("Run Full System Test"))
                {
                    RunFullSystemTest();
                }
                
                GUILayout.Space(10);
                
                GUILayout.Label($"FPS: {(1f / Time.unscaledDeltaTime):F1}");
                GUILayout.Label($"Quality: {QualitySettings.names[QualitySettings.GetQualityLevel()]}");
                
                GUILayout.EndVertical();
                GUILayout.EndArea();
            }
        }
    }
}