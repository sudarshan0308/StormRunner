using UnityEngine;
using System.Collections;

namespace StormRunner
{
    public class WeatherSystem : MonoBehaviour
    {
        [Header("Weather States")]
        [SerializeField] private WeatherState currentWeather = WeatherState.Clear;
        [SerializeField] private WeatherState targetWeather = WeatherState.Clear;
        [SerializeField] private float weatherTransitionTime = 5f;
        
        [Header("Rain System")]
        [SerializeField] private ParticleSystem rainParticles;
        [SerializeField] private AudioSource rainAudio;
        [SerializeField] private float rainIntensity = 0f;
        [SerializeField] private float maxRainIntensity = 1f;
        
        [Header("Lightning System")]
        [SerializeField] private Light directionalLight;
        [SerializeField] private AudioSource thunderAudio;
        [SerializeField] private AudioClip[] thunderSounds;
        [SerializeField] private float lightningIntensity = 0f;
        [SerializeField] private float lightningFrequency = 0.1f;
        
        [Header("Storm Effects")]
        [SerializeField] private AudioSource windAudio;
        [SerializeField] private AudioClip[] windSounds;
        [SerializeField] private float windIntensity = 0f;
        [SerializeField] private float maxWindIntensity = 1f;
        
        [Header("Post Processing")]
        [SerializeField] private Material skyboxMaterial;
        [SerializeField] private Color clearSkyColor = Color.cyan;
        [SerializeField] private Color stormSkyColor = Color.gray;
        
        [Header("Camera Effects")]
        [SerializeField] private CameraController cameraController;
        [SerializeField] private float stormCameraShakeIntensity = 0.5f;
        
        private Coroutine weatherTransitionCoroutine;
        private Coroutine lightningCoroutine;
        private float currentTransitionTime;
        
        private void Start()
        {
            InitializeWeather();
            StartCoroutine(WeatherCycle());
        }
        
        private void InitializeWeather()
        {
            if (rainParticles != null)
            {
                var emission = rainParticles.emission;
                emission.rateOverTime = 0;
            }
            
            if (directionalLight != null)
            {
                directionalLight.intensity = 1f;
            }
            
            SetWeather(WeatherState.Clear);
        }
        
        private void Update()
        {
            UpdateWeatherEffects();
            HandleWeatherInput();
        }
        
        private void UpdateWeatherEffects()
        {
            // Update rain intensity
            if (rainParticles != null)
            {
                var emission = rainParticles.emission;
                emission.rateOverTime = rainIntensity * 1000f;
                
                var main = rainParticles.main;
                main.startSpeed = rainIntensity * 20f + 5f;
            }
            
            // Update rain audio
            if (rainAudio != null)
            {
                rainAudio.volume = rainIntensity * 0.8f;
                rainAudio.pitch = 0.8f + rainIntensity * 0.4f;
            }
            
            // Update wind audio
            if (windAudio != null)
            {
                windAudio.volume = windIntensity * 0.6f;
                windAudio.pitch = 0.9f + windIntensity * 0.3f;
            }
            
            // Update lighting
            if (directionalLight != null)
            {
                float targetIntensity = 1f - (rainIntensity * 0.6f) - (lightningIntensity * 0.3f);
                directionalLight.intensity = Mathf.Lerp(directionalLight.intensity, targetIntensity, Time.deltaTime * 2f);
            }
            
            // Update skybox
            if (skyboxMaterial != null)
            {
                Color targetColor = Color.Lerp(clearSkyColor, stormSkyColor, rainIntensity);
                skyboxMaterial.SetColor("_SkyTint", targetColor);
            }
        }
        
        private void HandleWeatherInput()
        {
            if (Input.GetKeyDown(KeyCode.Alpha1))
                SetWeather(WeatherState.Clear);
            else if (Input.GetKeyDown(KeyCode.Alpha2))
                SetWeather(WeatherState.LightRain);
            else if (Input.GetKeyDown(KeyCode.Alpha3))
                SetWeather(WeatherState.HeavyRain);
            else if (Input.GetKeyDown(KeyCode.Alpha4))
                SetWeather(WeatherState.Storm);
        }
        
        public void SetWeather(WeatherState newWeather)
        {
            if (currentWeather == newWeather) return;
            
            targetWeather = newWeather;
            
            if (weatherTransitionCoroutine != null)
                StopCoroutine(weatherTransitionCoroutine);
            
            weatherTransitionCoroutine = StartCoroutine(TransitionWeather());
        }
        
        private IEnumerator TransitionWeather()
        {
            float startTime = Time.time;
            WeatherState startWeather = currentWeather;
            
            while (Time.time - startTime < weatherTransitionTime)
            {
                float t = (Time.time - startTime) / weatherTransitionTime;
                t = Mathf.SmoothStep(0f, 1f, t);
                
                // Interpolate weather parameters
                rainIntensity = Mathf.Lerp(GetWeatherRainIntensity(startWeather), GetWeatherRainIntensity(targetWeather), t);
                windIntensity = Mathf.Lerp(GetWeatherWindIntensity(startWeather), GetWeatherWindIntensity(targetWeather), t);
                lightningIntensity = Mathf.Lerp(GetWeatherLightningIntensity(startWeather), GetWeatherLightningIntensity(targetWeather), t);
                
                yield return null;
            }
            
            currentWeather = targetWeather;
            rainIntensity = GetWeatherRainIntensity(currentWeather);
            windIntensity = GetWeatherWindIntensity(currentWeather);
            lightningIntensity = GetWeatherLightningIntensity(currentWeather);
            
            // Start lightning if storm
            if (currentWeather == WeatherState.Storm)
            {
                if (lightningCoroutine != null)
                    StopCoroutine(lightningCoroutine);
                lightningCoroutine = StartCoroutine(LightningSequence());
            }
            else
            {
                if (lightningCoroutine != null)
                    StopCoroutine(lightningCoroutine);
            }
        }
        
        private IEnumerator LightningSequence()
        {
            while (currentWeather == WeatherState.Storm)
            {
                yield return new WaitForSeconds(Random.Range(2f, 8f));
                
                if (currentWeather == WeatherState.Storm)
                {
                    StartCoroutine(SingleLightning());
                }
            }
        }
        
        private IEnumerator SingleLightning()
        {
            // Flash lightning
            if (directionalLight != null)
            {
                float originalIntensity = directionalLight.intensity;
                directionalLight.intensity = 3f;
                
                yield return new WaitForSeconds(0.1f);
                
                directionalLight.intensity = originalIntensity;
                
                yield return new WaitForSeconds(0.1f);
                
                directionalLight.intensity = 2f;
                
                yield return new WaitForSeconds(0.05f);
                
                directionalLight.intensity = originalIntensity;
            }
            
            // Play thunder sound
            if (thunderAudio != null && thunderSounds.Length > 0)
            {
                AudioClip randomThunder = thunderSounds[Random.Range(0, thunderSounds.Length)];
                thunderAudio.PlayOneShot(randomThunder);
                
                // Camera shake
                if (cameraController != null)
                {
                    cameraController.ShakeCamera(stormCameraShakeIntensity, 0.5f);
                }
            }
        }
        
        private IEnumerator WeatherCycle()
        {
            while (true)
            {
                // Random weather changes
                yield return new WaitForSeconds(Random.Range(30f, 120f));
                
                if (Random.value < 0.3f)
                {
                    WeatherState[] possibleWeathers = { WeatherState.LightRain, WeatherState.HeavyRain, WeatherState.Storm };
                    WeatherState randomWeather = possibleWeathers[Random.Range(0, possibleWeathers.Length)];
                    SetWeather(randomWeather);
                }
                else
                {
                    SetWeather(WeatherState.Clear);
                }
            }
        }
        
        private float GetWeatherRainIntensity(WeatherState weather)
        {
            switch (weather)
            {
                case WeatherState.Clear: return 0f;
                case WeatherState.LightRain: return 0.3f;
                case WeatherState.HeavyRain: return 0.7f;
                case WeatherState.Storm: return 1f;
                default: return 0f;
            }
        }
        
        private float GetWeatherWindIntensity(WeatherState weather)
        {
            switch (weather)
            {
                case WeatherState.Clear: return 0f;
                case WeatherState.LightRain: return 0.2f;
                case WeatherState.HeavyRain: return 0.5f;
                case WeatherState.Storm: return 1f;
                default: return 0f;
            }
        }
        
        private float GetWeatherLightningIntensity(WeatherState weather)
        {
            switch (weather)
            {
                case WeatherState.Clear: return 0f;
                case WeatherState.LightRain: return 0f;
                case WeatherState.HeavyRain: return 0.3f;
                case WeatherState.Storm: return 1f;
                default: return 0f;
            }
        }
        
        public WeatherState GetCurrentWeather()
        {
            return currentWeather;
        }
        
        public float GetRainIntensity()
        {
            return rainIntensity;
        }
        
        public float GetWindIntensity()
        {
            return windIntensity;
        }
        
        public float GetLightningIntensity()
        {
            return lightningIntensity;
        }
    }
    
    public enum WeatherState
    {
        Clear,
        LightRain,
        HeavyRain,
        Storm
    }
}
