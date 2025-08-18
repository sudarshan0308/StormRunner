using UnityEngine;
#if UNITY_EDITOR
using UnityEditor;
using UnityEditor.Build.Reporting;
#endif

namespace StormRunner
{
    public class BuildManager : MonoBehaviour
    {
#if UNITY_EDITOR
        [Header("Build Settings")]
        [SerializeField] private string buildPath = "Builds/";
        [SerializeField] private string productName = "StormRunner";
        [SerializeField] private string companyName = "StormRunner Studios";
        [SerializeField] private string version = "1.0.0";
        
        [Header("Platform Settings")]
        [SerializeField] private bool buildWindows = true;
        [SerializeField] private bool buildAndroid = true;
        [SerializeField] private bool buildIOS = true;
        
        [MenuItem("StormRunner/Build All Platforms")]
        public static void BuildAllPlatforms()
        {
            BuildManager buildManager = FindObjectOfType<BuildManager>();
            if (buildManager == null)
            {
                Debug.LogError("BuildManager not found in scene!");
                return;
            }
            
            buildManager.PerformBuildAll();
        }
        
        [MenuItem("StormRunner/Build Windows")]
        public static void BuildWindows()
        {
            BuildManager buildManager = FindObjectOfType<BuildManager>();
            if (buildManager == null)
            {
                Debug.LogError("BuildManager not found in scene!");
                return;
            }
            
            buildManager.PerformBuildWindows();
        }
        
        [MenuItem("StormRunner/Build Android")]
        public static void BuildAndroid()
        {
            BuildManager buildManager = FindObjectOfType<BuildManager>();
            if (buildManager == null)
            {
                Debug.LogError("BuildManager not found in scene!");
                return;
            }
            
            buildManager.PerformBuildAndroid();
        }
        
        public void PerformBuildAll()
        {
            SetupPlayerSettings();
            
            if (buildWindows)
                PerformBuildWindows();
            
            if (buildAndroid)
                PerformBuildAndroid();
            
            if (buildIOS)
                PerformBuildIOS();
        }
        
        public void PerformBuildWindows()
        {
            Debug.Log("Starting Windows build...");
            
            BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
            buildPlayerOptions.scenes = GetScenePaths();
            buildPlayerOptions.locationPathName = buildPath + "Windows/" + productName + ".exe";
            buildPlayerOptions.target = BuildTarget.StandaloneWindows64;
            buildPlayerOptions.options = BuildOptions.None;
            
            BuildReport report = BuildPipeline.BuildPlayer(buildPlayerOptions);
            BuildSummary summary = report.summary;
            
            if (summary.result == BuildResult.Succeeded)
            {
                Debug.Log("Windows build succeeded: " + summary.totalSize + " bytes");
            }
            
            if (summary.result == BuildResult.Failed)
            {
                Debug.Log("Windows build failed");
            }
        }
        
        public void PerformBuildAndroid()
        {
            Debug.Log("Starting Android build...");
            
            // Set Android specific settings
            PlayerSettings.Android.minSdkVersion = AndroidSdkVersions.AndroidApiLevel24;
            PlayerSettings.Android.targetSdkVersion = AndroidSdkVersions.AndroidApiLevel33;
            PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARM64;
            
            BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
            buildPlayerOptions.scenes = GetScenePaths();
            buildPlayerOptions.locationPathName = buildPath + "Android/" + productName + ".apk";
            buildPlayerOptions.target = BuildTarget.Android;
            buildPlayerOptions.options = BuildOptions.None;
            
            BuildReport report = BuildPipeline.BuildPlayer(buildPlayerOptions);
            BuildSummary summary = report.summary;
            
            if (summary.result == BuildResult.Succeeded)
            {
                Debug.Log("Android build succeeded: " + summary.totalSize + " bytes");
            }
            
            if (summary.result == BuildResult.Failed)
            {
                Debug.Log("Android build failed");
            }
        }
        
        public void PerformBuildIOS()
        {
            Debug.Log("Starting iOS build...");
            
            // Set iOS specific settings
            PlayerSettings.iOS.targetOSVersionString = "12.0";
            PlayerSettings.iOS.targetDevice = iOSTargetDevice.iPhoneAndiPad;
            
            BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
            buildPlayerOptions.scenes = GetScenePaths();
            buildPlayerOptions.locationPathName = buildPath + "iOS/";
            buildPlayerOptions.target = BuildTarget.iOS;
            buildPlayerOptions.options = BuildOptions.None;
            
            BuildReport report = BuildPipeline.BuildPlayer(buildPlayerOptions);
            BuildSummary summary = report.summary;
            
            if (summary.result == BuildResult.Succeeded)
            {
                Debug.Log("iOS build succeeded: " + summary.totalSize + " bytes");
            }
            
            if (summary.result == BuildResult.Failed)
            {
                Debug.Log("iOS build failed");
            }
        }
        
        private void SetupPlayerSettings()
        {
            PlayerSettings.productName = productName;
            PlayerSettings.companyName = companyName;
            PlayerSettings.bundleVersion = version;
            
            // Set bundle identifier for mobile platforms
            PlayerSettings.SetApplicationIdentifier(BuildTargetGroup.Android, "com.stormrunnerstudios.stormrunner");
            PlayerSettings.SetApplicationIdentifier(BuildTargetGroup.iOS, "com.stormrunnerstudios.stormrunner");
            
            // Graphics settings
            PlayerSettings.colorSpace = ColorSpace.Linear;
            PlayerSettings.SetGraphicsAPIs(BuildTarget.Android, new UnityEngine.Rendering.GraphicsDeviceType[] { 
                UnityEngine.Rendering.GraphicsDeviceType.OpenGLES3,
                UnityEngine.Rendering.GraphicsDeviceType.Vulkan 
            });
            
            // Quality settings
            QualitySettings.SetQualityLevel(2, true); // High quality
        }
        
        private string[] GetScenePaths()
        {
            EditorBuildSettingsScene[] scenes = EditorBuildSettings.scenes;
            string[] scenePaths = new string[scenes.Length];
            
            for (int i = 0; i < scenes.Length; i++)
            {
                scenePaths[i] = scenes[i].path;
            }
            
            return scenePaths;
        }
#endif
    }
}