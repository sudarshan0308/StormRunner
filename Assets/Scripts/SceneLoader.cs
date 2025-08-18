using UnityEngine;
using UnityEngine.SceneManagement;
using System.Collections;

namespace StormRunner
{
    public class SceneLoader : MonoBehaviour
    {
        [Header("Loading Screen")]
        [SerializeField] private GameObject loadingScreen;
        [SerializeField] private UnityEngine.UI.Slider progressBar;
        [SerializeField] private TMPro.TextMeshProUGUI loadingText;
        [SerializeField] private string[] loadingTips;
        
        [Header("Fade Settings")]
        [SerializeField] private CanvasGroup fadeCanvasGroup;
        [SerializeField] private float fadeDuration = 1f;
        
        private static SceneLoader instance;
        
        public static SceneLoader Instance
        {
            get
            {
                if (instance == null)
                {
                    GameObject sceneLoaderObj = new GameObject("SceneLoader");
                    instance = sceneLoaderObj.AddComponent<SceneLoader>();
                    DontDestroyOnLoad(sceneLoaderObj);
                }
                return instance;
            }
        }
        
        private void Awake()
        {
            if (instance == null)
            {
                instance = this;
                DontDestroyOnLoad(gameObject);
            }
            else if (instance != this)
            {
                Destroy(gameObject);
            }
        }
        
        public void LoadScene(string sceneName)
        {
            StartCoroutine(LoadSceneAsync(sceneName));
        }
        
        public void LoadScene(int sceneIndex)
        {
            StartCoroutine(LoadSceneAsync(sceneIndex));
        }
        
        private IEnumerator LoadSceneAsync(string sceneName)
        {
            // Show loading screen
            if (loadingScreen != null)
                loadingScreen.SetActive(true);
            
            // Fade out
            yield return StartCoroutine(FadeOut());
            
            // Start loading
            AsyncOperation asyncLoad = SceneManager.LoadSceneAsync(sceneName);
            asyncLoad.allowSceneActivation = false;
            
            // Update progress
            while (!asyncLoad.isDone)
            {
                float progress = Mathf.Clamp01(asyncLoad.progress / 0.9f);
                
                if (progressBar != null)
                    progressBar.value = progress;
                
                if (loadingText != null)
                {
                    if (loadingTips.Length > 0)
                    {
                        int tipIndex = Random.Range(0, loadingTips.Length);
                        loadingText.text = loadingTips[tipIndex];
                    }
                    else
                    {
                        loadingText.text = $"Loading... {(progress * 100):F0}%";
                    }
                }
                
                if (asyncLoad.progress >= 0.9f)
                {
                    if (progressBar != null)
                        progressBar.value = 1f;
                    
                    asyncLoad.allowSceneActivation = true;
                }
                
                yield return null;
            }
            
            // Fade in
            yield return StartCoroutine(FadeIn());
            
            // Hide loading screen
            if (loadingScreen != null)
                loadingScreen.SetActive(false);
        }
        
        private IEnumerator LoadSceneAsync(int sceneIndex)
        {
            // Show loading screen
            if (loadingScreen != null)
                loadingScreen.SetActive(true);
            
            // Fade out
            yield return StartCoroutine(FadeOut());
            
            // Start loading
            AsyncOperation asyncLoad = SceneManager.LoadSceneAsync(sceneIndex);
            asyncLoad.allowSceneActivation = false;
            
            // Update progress
            while (!asyncLoad.isDone)
            {
                float progress = Mathf.Clamp01(asyncLoad.progress / 0.9f);
                
                if (progressBar != null)
                    progressBar.value = progress;
                
                if (loadingText != null)
                {
                    if (loadingTips.Length > 0)
                    {
                        int tipIndex = Random.Range(0, loadingTips.Length);
                        loadingText.text = loadingTips[tipIndex];
                    }
                    else
                    {
                        loadingText.text = $"Loading... {(progress * 100):F0}%";
                    }
                }
                
                if (asyncLoad.progress >= 0.9f)
                {
                    if (progressBar != null)
                        progressBar.value = 1f;
                    
                    asyncLoad.allowSceneActivation = true;
                }
                
                yield return null;
            }
            
            // Fade in
            yield return StartCoroutine(FadeIn());
            
            // Hide loading screen
            if (loadingScreen != null)
                loadingScreen.SetActive(false);
        }
        
        private IEnumerator FadeOut()
        {
            if (fadeCanvasGroup == null) yield break;
            
            float elapsedTime = 0f;
            float startAlpha = fadeCanvasGroup.alpha;
            
            while (elapsedTime < fadeDuration)
            {
                elapsedTime += Time.deltaTime;
                fadeCanvasGroup.alpha = Mathf.Lerp(startAlpha, 1f, elapsedTime / fadeDuration);
                yield return null;
            }
            
            fadeCanvasGroup.alpha = 1f;
        }
        
        private IEnumerator FadeIn()
        {
            if (fadeCanvasGroup == null) yield break;
            
            float elapsedTime = 0f;
            float startAlpha = fadeCanvasGroup.alpha;
            
            while (elapsedTime < fadeDuration)
            {
                elapsedTime += Time.deltaTime;
                fadeCanvasGroup.alpha = Mathf.Lerp(startAlpha, 0f, elapsedTime / fadeDuration);
                yield return null;
            }
            
            fadeCanvasGroup.alpha = 0f;
        }
    }
}