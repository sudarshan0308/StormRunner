using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

namespace StormRunner
{
    public class PerformanceManager : MonoBehaviour
    {
        [Header("Performance Settings")]
        [SerializeField] private bool enableDynamicQuality = true;
        [SerializeField] private float targetFrameRate = 60f;
        [SerializeField] private float qualityCheckInterval = 2f;
        
        [Header("Quality Levels")]
        [SerializeField] private int lowQualityLevel = 0;
        [SerializeField] private int mediumQualityLevel = 1;
        [SerializeField] private int highQualityLevel = 2;
        
        [Header("Performance Thresholds")]
        [SerializeField] private float lowFPSThreshold = 30f;
        [SerializeField] private float highFPSThreshold = 55f;
        
        private float frameRateSum = 0f;
        private int frameCount = 0;
        private float lastQualityCheck = 0f;
        private int currentQualityLevel;
        
        private void Start()
        {
            InitializePerformanceSettings();
            currentQualityLevel = QualitySettings.GetQualityLevel();
        }
        
        private void InitializePerformanceSettings()
        {
            // Set target frame rate
            Application.targetFrameRate = (int)targetFrameRate;
            
            // Enable VSync on desktop, disable on mobile for better performance control
            #if UNITY_STANDALONE
                QualitySettings.vSyncCount = 1;
            #else
                QualitySettings.vSyncCount = 0;
            #endif
            
            // Set initial quality based on platform
            #if UNITY_ANDROID || UNITY_IOS
                QualitySettings.SetQualityLevel(mediumQualityLevel, true);
            #else
                QualitySettings.SetQualityLevel(highQualityLevel, true);
            #endif
        }
        
        private void Update()
        {
            if (enableDynamicQuality)
            {
                TrackFrameRate();
                CheckQualityAdjustment();
            }
        }
        
        private void TrackFrameRate()
        {
            frameRateSum += 1f / Time.unscaledDeltaTime;
            frameCount++;
        }
        
        private void CheckQualityAdjustment()
        {
            if (Time.time - lastQualityCheck >= qualityCheckInterval && frameCount > 0)
            {
                float averageFPS = frameRateSum / frameCount;
                
                if (averageFPS < lowFPSThreshold && currentQualityLevel > lowQualityLevel)
                {
                    // Decrease quality
                    currentQualityLevel = Mathf.Max(lowQualityLevel, currentQualityLevel - 1);
                    QualitySettings.SetQualityLevel(currentQualityLevel, true);
                    Debug.Log($"Performance: Decreased quality to level {currentQualityLevel} (FPS: {averageFPS:F1})");
                }
                else if (averageFPS > highFPSThreshold && currentQualityLevel < highQualityLevel)
                {
                    // Increase quality
                    currentQualityLevel = Mathf.Min(highQualityLevel, currentQualityLevel + 1);
                    QualitySettings.SetQualityLevel(currentQualityLevel, true);
                    Debug.Log($"Performance: Increased quality to level {currentQualityLevel} (FPS: {averageFPS:F1})");
                }
                
                // Reset tracking
                frameRateSum = 0f;
                frameCount = 0;
                lastQualityCheck = Time.time;
            }
        }
        
        public void SetQualityLevel(int level)
        {
            currentQualityLevel = Mathf.Clamp(level, lowQualityLevel, highQualityLevel);
            QualitySettings.SetQualityLevel(currentQualityLevel, true);
            Debug.Log($"Performance: Manual quality set to level {currentQualityLevel}");
        }
        
        public void EnableDynamicQuality(bool enable)
        {
            enableDynamicQuality = enable;
            Debug.Log($"Performance: Dynamic quality {(enable ? "enabled" : "disabled")}");
        }
        
        public float GetCurrentFPS()
        {
            return frameCount > 0 ? frameRateSum / frameCount : 0f;
        }
        
        public int GetCurrentQualityLevel()
        {
            return currentQualityLevel;
        }
        
        private void OnGUI()
        {
            if (Debug.isDebugBuild)
            {
                GUI.Label(new Rect(10, 10, 200, 20), $"FPS: {(1f / Time.unscaledDeltaTime):F1}");
                GUI.Label(new Rect(10, 30, 200, 20), $"Quality: {QualitySettings.names[currentQualityLevel]}");
                GUI.Label(new Rect(10, 50, 200, 20), $"Dynamic: {enableDynamicQuality}");
            }
        }
    }
}