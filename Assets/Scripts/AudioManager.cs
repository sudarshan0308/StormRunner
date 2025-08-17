using UnityEngine;
using UnityEngine.Audio;
using System.Collections;
using System.Collections.Generic;

namespace StormRunner
{
    public class AudioManager : MonoBehaviour
    {
        [Header("Audio Sources")]
        [SerializeField] private AudioSource musicSource;
        [SerializeField] private AudioSource sfxSource;
        [SerializeField] private AudioSource ambientSource;
        [SerializeField] private AudioSource weatherSource;
        
        [Header("Audio Mixers")]
        [SerializeField] private AudioMixer masterMixer;
        [SerializeField] private AudioMixerGroup musicGroup;
        [SerializeField] private AudioMixerGroup sfxGroup;
        [SerializeField] private AudioMixerGroup ambientGroup;
        [SerializeField] private AudioMixerGroup weatherGroup;
        
        [Header("Audio Clips")]
        [SerializeField] private AudioClip[] musicTracks;
        [SerializeField] private AudioClip[] ambientSounds;
        [SerializeField] private AudioClip[] weatherSounds;
        [SerializeField] private AudioClip[] footstepSounds;
        [SerializeField] private AudioClip[] jumpSounds;
        [SerializeField] private AudioClip[] interactionSounds;
        
        [Header("Weather Audio")]
        [SerializeField] private AudioClip lightRainSound;
        [SerializeField] private AudioClip heavyRainSound;
        [SerializeField] private AudioClip stormSound;
        [SerializeField] private AudioClip windSound;
        [SerializeField] private AudioClip thunderSound;
        
        [Header("Audio Settings")]
        [SerializeField] private float masterVolume = 1f;
        [SerializeField] private float musicVolume = 0.7f;
        [SerializeField] private float sfxVolume = 1f;
        [SerializeField] private float ambientVolume = 0.5f;
        [SerializeField] private float weatherVolume = 0.8f;
        
        [Header("Dynamic Audio")]
        [SerializeField] private bool enableDynamicAudio = true;
        [SerializeField] private float weatherTransitionTime = 2f;
        [SerializeField] private float musicCrossfadeTime = 3f;
        
        [Header("Dolby Settings")]
        [SerializeField] private bool enableDolbyAudio = true;
        [SerializeField] private float dolbyIntensity = 0.8f;
        [SerializeField] private float spatialBlend = 1f;
        
        private Dictionary<string, AudioClip> audioClipDictionary;
        private Coroutine weatherAudioCoroutine;
        private Coroutine musicCrossfadeCoroutine;
        private WeatherSystem weatherSystem;
        private int currentMusicIndex = 0;
        
        private void Awake()
        {
            InitializeAudioSources();
            SetupAudioMixers();
            CreateAudioClipDictionary();
            LoadAudioSettings();
        }
        
        private void Start()
        {
            weatherSystem = FindObjectOfType<WeatherSystem>();
            StartAmbientAudio();
            StartMusicPlaylist();
        }
        
        private void InitializeAudioSources()
        {
            // Create audio sources if they don't exist
            if (musicSource == null)
            {
                GameObject musicObj = new GameObject("MusicSource");
                musicObj.transform.SetParent(transform);
                musicSource = musicObj.AddComponent<AudioSource>();
                musicSource.loop = true;
                musicSource.playOnAwake = false;
            }
            
            if (sfxSource == null)
            {
                GameObject sfxObj = new GameObject("SFXSource");
                sfxObj.transform.SetParent(transform);
                sfxSource = sfxObj.AddComponent<AudioSource>();
                sfxSource.playOnAwake = false;
            }
            
            if (ambientSource == null)
            {
                GameObject ambientObj = new GameObject("AmbientSource");
                ambientObj.transform.SetParent(transform);
                ambientSource = ambientObj.AddComponent<AudioSource>();
                ambientSource.loop = true;
                ambientSource.playOnAwake = false;
            }
            
            if (weatherSource == null)
            {
                GameObject weatherObj = new GameObject("WeatherSource");
                weatherObj.transform.SetParent(transform);
                weatherSource = weatherObj.AddComponent<AudioSource>();
                weatherSource.loop = true;
                weatherSource.playOnAwake = false;
            }
        }
        
        private void SetupAudioMixers()
        {
            if (masterMixer != null)
            {
                // Set up mixer groups
                if (musicGroup != null)
                    musicSource.outputAudioMixerGroup = musicGroup;
                
                if (sfxGroup != null)
                    sfxSource.outputAudioMixerGroup = sfxGroup;
                
                if (ambientGroup != null)
                    ambientSource.outputAudioMixerGroup = ambientGroup;
                
                if (weatherGroup != null)
                    weatherSource.outputAudioMixerGroup = weatherGroup;
            }
            
            // Apply Dolby settings
            if (enableDolbyAudio)
            {
                ApplyDolbySettings();
            }
        }
        
        private void ApplyDolbySettings()
        {
            // Set spatial blend for 3D audio
            musicSource.spatialBlend = 0f; // 2D music
            sfxSource.spatialBlend = spatialBlend;
            ambientSource.spatialBlend = spatialBlend;
            weatherSource.spatialBlend = 0f; // 2D weather
            
            // Apply Dolby effects through mixer
            if (masterMixer != null)
            {
                masterMixer.SetFloat("DolbyIntensity", dolbyIntensity);
                masterMixer.SetFloat("SpatialBlend", spatialBlend);
            }
        }
        
        private void CreateAudioClipDictionary()
        {
            audioClipDictionary = new Dictionary<string, AudioClip>();
            
            // Add all audio clips to dictionary for easy access
            if (footstepSounds != null)
            {
                foreach (AudioClip clip in footstepSounds)
                {
                    if (clip != null)
                        audioClipDictionary[clip.name] = clip;
                }
            }
            
            if (jumpSounds != null)
            {
                foreach (AudioClip clip in jumpSounds)
                {
                    if (clip != null)
                        audioClipDictionary[clip.name] = clip;
                }
            }
            
            if (interactionSounds != null)
            {
                foreach (AudioClip clip in interactionSounds)
                {
                    if (clip != null)
                        audioClipDictionary[clip.name] = clip;
                }
            }
        }
        
        private void LoadAudioSettings()
        {
            masterVolume = PlayerPrefs.GetFloat("MasterVolume", 1f);
            musicVolume = PlayerPrefs.GetFloat("MusicVolume", 0.7f);
            sfxVolume = PlayerPrefs.GetFloat("SFXVolume", 1f);
            ambientVolume = PlayerPrefs.GetFloat("AmbientVolume", 0.5f);
            weatherVolume = PlayerPrefs.GetFloat("WeatherVolume", 0.8f);
            
            ApplyVolumeSettings();
        }
        
        private void ApplyVolumeSettings()
        {
            if (masterMixer != null)
            {
                masterMixer.SetFloat("MasterVolume", Mathf.Log10(masterVolume) * 20f);
                masterMixer.SetFloat("MusicVolume", Mathf.Log10(musicVolume) * 20f);
                masterMixer.SetFloat("SFXVolume", Mathf.Log10(sfxVolume) * 20f);
                masterMixer.SetFloat("AmbientVolume", Mathf.Log10(ambientVolume) * 20f);
                masterMixer.SetFloat("WeatherVolume", Mathf.Log10(weatherVolume) * 20f);
            }
        }
        
        private void StartAmbientAudio()
        {
            if (ambientSource != null && ambientSounds.Length > 0)
            {
                AudioClip randomAmbient = ambientSounds[Random.Range(0, ambientSounds.Length)];
                ambientSource.clip = randomAmbient;
                ambientSource.volume = ambientVolume;
                ambientSource.Play();
            }
        }
        
        private void StartMusicPlaylist()
        {
            if (musicSource != null && musicTracks.Length > 0)
            {
                PlayMusicTrack(0);
            }
        }
        
        private void PlayMusicTrack(int index)
        {
            if (musicTracks == null || index >= musicTracks.Length) return;
            
            if (musicCrossfadeCoroutine != null)
                StopCoroutine(musicCrossfadeCoroutine);
            
            musicCrossfadeCoroutine = StartCoroutine(CrossfadeMusic(musicTracks[index]));
            currentMusicIndex = index;
        }
        
        private IEnumerator CrossfadeMusic(AudioClip newTrack)
        {
            AudioSource tempSource = gameObject.AddComponent<AudioSource>();
            tempSource.clip = newTrack;
            tempSource.volume = 0f;
            tempSource.loop = true;
            tempSource.outputAudioMixerGroup = musicSource.outputAudioMixerGroup;
            
            tempSource.Play();
            
            float elapsed = 0f;
            float startVolume = musicSource.volume;
            
            while (elapsed < musicCrossfadeTime)
            {
                elapsed += Time.deltaTime;
                float t = elapsed / musicCrossfadeTime;
                
                musicSource.volume = Mathf.Lerp(startVolume, 0f, t);
                tempSource.volume = Mathf.Lerp(0f, musicVolume, t);
                
                yield return null;
            }
            
            musicSource.Stop();
            musicSource.clip = newTrack;
            musicSource.volume = musicVolume;
            musicSource.Play();
            
            Destroy(tempSource);
        }
        
        public void PlaySFX(string clipName, float volume = 1f, float pitch = 1f)
        {
            if (audioClipDictionary.ContainsKey(clipName))
            {
                PlaySFX(audioClipDictionary[clipName], volume, pitch);
            }
        }
        
        public void PlaySFX(AudioClip clip, float volume = 1f, float pitch = 1f)
        {
            if (clip != null && sfxSource != null)
            {
                sfxSource.PlayOneShot(clip, volume * sfxVolume);
                sfxSource.pitch = pitch;
            }
        }
        
        public void PlayFootstep()
        {
            if (footstepSounds.Length > 0)
            {
                AudioClip randomFootstep = footstepSounds[Random.Range(0, footstepSounds.Length)];
                PlaySFX(randomFootstep, 0.8f, Random.Range(0.9f, 1.1f));
            }
        }
        
        public void PlayJump()
        {
            if (jumpSounds.Length > 0)
            {
                AudioClip randomJump = jumpSounds[Random.Range(0, jumpSounds.Length)];
                PlaySFX(randomJump, 1f, Random.Range(0.95f, 1.05f));
            }
        }
        
        public void PlayInteraction()
        {
            if (interactionSounds.Length > 0)
            {
                AudioClip randomInteraction = interactionSounds[Random.Range(0, interactionSounds.Length)];
                PlaySFX(randomInteraction, 0.9f, 1f);
            }
        }
        
        public void UpdateWeatherAudio(WeatherState weatherState)
        {
            if (weatherAudioCoroutine != null)
                StopCoroutine(weatherAudioCoroutine);
            
            weatherAudioCoroutine = StartCoroutine(TransitionWeatherAudio(weatherState));
        }
        
        private IEnumerator TransitionWeatherAudio(WeatherState newWeather)
        {
            AudioClip targetClip = GetWeatherAudioClip(newWeather);
            if (targetClip == null) yield break;
            
            float startVolume = weatherSource.volume;
            float elapsed = 0f;
            
            while (elapsed < weatherTransitionTime)
            {
                elapsed += Time.deltaTime;
                float t = elapsed / weatherTransitionTime;
                
                weatherSource.volume = Mathf.Lerp(startVolume, weatherVolume, t);
                
                yield return null;
            }
            
            weatherSource.clip = targetClip;
            weatherSource.volume = weatherVolume;
            weatherSource.Play();
        }
        
        private AudioClip GetWeatherAudioClip(WeatherState weather)
        {
            switch (weather)
            {
                case WeatherState.Clear:
                    return null;
                case WeatherState.LightRain:
                    return lightRainSound;
                case WeatherState.HeavyRain:
                    return heavyRainSound;
                case WeatherState.Storm:
                    return stormSound;
                default:
                    return null;
            }
        }
        
        public void SetMasterVolume(float volume)
        {
            masterVolume = volume;
            PlayerPrefs.SetFloat("MasterVolume", volume);
            PlayerPrefs.Save();
            ApplyVolumeSettings();
        }
        
        public void SetMusicVolume(float volume)
        {
            musicVolume = volume;
            PlayerPrefs.SetFloat("MusicVolume", volume);
            PlayerPrefs.Save();
            ApplyVolumeSettings();
        }
        
        public void SetSFXVolume(float volume)
        {
            sfxVolume = volume;
            PlayerPrefs.SetFloat("SFXVolume", volume);
            PlayerPrefs.Save();
            ApplyVolumeSettings();
        }
        
        public void SetAmbientVolume(float volume)
        {
            ambientVolume = volume;
            PlayerPrefs.SetFloat("AmbientVolume", volume);
            PlayerPrefs.Save();
            ApplyVolumeSettings();
        }
        
        public void SetWeatherVolume(float volume)
        {
            weatherVolume = volume;
            PlayerPrefs.SetFloat("WeatherVolume", volume);
            PlayerPrefs.Save();
            ApplyVolumeSettings();
        }
        
        public void NextMusicTrack()
        {
            if (musicTracks.Length > 0)
            {
                int nextIndex = (currentMusicIndex + 1) % musicTracks.Length;
                PlayMusicTrack(nextIndex);
            }
        }
        
        public void PreviousMusicTrack()
        {
            if (musicTracks.Length > 0)
            {
                int prevIndex = (currentMusicIndex - 1 + musicTracks.Length) % musicTracks.Length;
                PlayMusicTrack(prevIndex);
            }
        }
        
        public void StopAllAudio()
        {
            if (musicSource != null) musicSource.Stop();
            if (sfxSource != null) sfxSource.Stop();
            if (ambientSource != null) ambientSource.Stop();
            if (weatherSource != null) weatherSource.Stop();
        }
        
        public void PauseAllAudio()
        {
            if (musicSource != null) musicSource.Pause();
            if (sfxSource != null) sfxSource.Pause();
            if (ambientSource != null) ambientSource.Pause();
            if (weatherSource != null) weatherSource.Pause();
        }
        
        public void ResumeAllAudio()
        {
            if (musicSource != null) musicSource.UnPause();
            if (sfxSource != null) sfxSource.UnPause();
            if (ambientSource != null) ambientSource.UnPause();
            if (weatherSource != null) weatherSource.UnPause();
        }
        
        private void Update()
        {
            // Auto-advance music playlist
            if (musicSource != null && !musicSource.isPlaying && musicTracks.Length > 0)
            {
                NextMusicTrack();
            }
            
            // Update weather audio based on weather system
            if (weatherSystem != null && enableDynamicAudio)
            {
                UpdateWeatherAudio(weatherSystem.GetCurrentWeather());
            }
        }
        
        private void OnDestroy()
        {
            if (weatherAudioCoroutine != null)
                StopCoroutine(weatherAudioCoroutine);
            
            if (musicCrossfadeCoroutine != null)
                StopCoroutine(musicCrossfadeCoroutine);
        }
    }
}
