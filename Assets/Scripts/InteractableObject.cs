using UnityEngine;

namespace StormRunner
{
    public class InteractableObject : MonoBehaviour, IInteractable
    {
        [Header("Interaction Settings")]
        [SerializeField] private string interactionText = "Press E to interact";
        [SerializeField] private float interactionRange = 3f;
        [SerializeField] private bool isOneTimeUse = false;
        [SerializeField] private GameObject highlightEffect;
        
        [Header("Audio")]
        [SerializeField] private AudioSource audioSource;
        [SerializeField] private AudioClip interactionSound;
        
        private bool hasBeenUsed = false;
        private bool playerInRange = false;
        private UIManager uiManager;
        
        private void Start()
        {
            uiManager = FindObjectOfType<UIManager>();
            
            if (audioSource == null)
            {
                audioSource = gameObject.AddComponent<AudioSource>();
                audioSource.playOnAwake = false;
            }
            
            if (highlightEffect != null)
                highlightEffect.SetActive(false);
        }
        
        private void Update()
        {
            CheckPlayerDistance();
        }
        
        private void CheckPlayerDistance()
        {
            PlayerController player = FindObjectOfType<PlayerController>();
            if (player == null) return;
            
            float distance = Vector3.Distance(transform.position, player.transform.position);
            bool wasInRange = playerInRange;
            playerInRange = distance <= interactionRange;
            
            if (playerInRange && !wasInRange && !hasBeenUsed)
            {
                OnPlayerEnterRange();
            }
            else if (!playerInRange && wasInRange)
            {
                OnPlayerExitRange();
            }
        }
        
        private void OnPlayerEnterRange()
        {
            if (highlightEffect != null)
                highlightEffect.SetActive(true);
            
            if (uiManager != null)
                uiManager.ShowInteractionPrompt(interactionText);
        }
        
        private void OnPlayerExitRange()
        {
            if (highlightEffect != null)
                highlightEffect.SetActive(false);
            
            if (uiManager != null)
                uiManager.HideInteractionPrompt();
        }
        
        public virtual void Interact(PlayerController player)
        {
            if (hasBeenUsed && isOneTimeUse) return;
            
            // Play interaction sound
            if (audioSource != null && interactionSound != null)
            {
                audioSource.PlayOneShot(interactionSound);
            }
            
            // Play interaction sound through AudioManager
            AudioManager audioManager = FindObjectOfType<AudioManager>();
            if (audioManager != null)
            {
                audioManager.PlayInteraction();
            }
            
            // Perform interaction
            OnInteract(player);
            
            if (isOneTimeUse)
            {
                hasBeenUsed = true;
                OnPlayerExitRange();
            }
        }
        
        protected virtual void OnInteract(PlayerController player)
        {
            // Override this method in derived classes for specific interactions
            Debug.Log($"Interacted with {gameObject.name}");
        }
        
        private void OnDrawGizmosSelected()
        {
            Gizmos.color = Color.yellow;
            Gizmos.DrawWireSphere(transform.position, interactionRange);
        }
    }
}