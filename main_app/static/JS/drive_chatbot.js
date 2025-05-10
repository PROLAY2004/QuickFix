document.addEventListener('DOMContentLoaded', function() {
    const chatbotContainer = document.querySelector('.chatbot-container');
    const converterBtn = document.querySelector('.drive-converter-btn');
    const closeChatbot = document.querySelector('.close-chatbot');
    const convertBtn = document.getElementById('convert-btn');
    const driveLinkInput = document.getElementById('drive-link');
    const chatbotMessages = document.querySelector('.chatbot-messages');
    
    // Initialize chatbot as hidden
    chatbotContainer.style.display = 'none';
    
    // Enhanced toggle function
    function toggleChatbot(forceClose = false) {
        if (forceClose) {
            chatbotContainer.style.display = 'none';
            chatbotContainer.classList.remove('active');
        } else {
            if (chatbotContainer.classList.contains('active')) {
                chatbotContainer.classList.remove('active');
                setTimeout(() => {
                    chatbotContainer.style.display = 'none';
                }, 300);
            } else {
                chatbotContainer.style.display = 'block';
                setTimeout(() => {
                    chatbotContainer.classList.add('active');
                    driveLinkInput.focus();
                }, 10);
            }
        }
    }
    
    // Event listeners
    converterBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleChatbot();
    });
    
    closeChatbot.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleChatbot(true);
    });
    
    document.addEventListener('click', function(e) {
        if (!chatbotContainer.contains(e.target)) {
            toggleChatbot(true);
        }
    });
    
    chatbotContainer.addEventListener('click', function(e) {
        e.stopPropagation();
    });
    
    // Convert Google Drive link (multiple times)
    function convertDriveLink() {
        const driveLink = driveLinkInput.value.trim();
        
        if (!driveLink) {
            addBotMessage('Please enter a Google Drive link');
            return;
        }
        
        const fileId = extractFileId(driveLink);
        
        if (!fileId) {
            addBotMessage('Invalid Google Drive link format. Please check and try again.');
            return;
        }
        
        addUserMessage(driveLink);
        
        const apiKey = "AIzaSyDeoyWqRG9_wqLkRiZ-waSpkQna7OeeC54";
        const directLink = `https://www.googleapis.com/drive/v3/files/${fileId}?alt=media&key=${apiKey}`;
        
        showResultMessage(directLink);
        
        // Clear input but keep the field available for new conversions
        driveLinkInput.value = '';
        driveLinkInput.focus();
    }
    
    function extractFileId(driveLink) {
        const patterns = [
            /\/file\/d\/([^\/]+)/,
            /id=([^&]+)/,
            /[-\w]{25,}/
        ];
        
        for (const pattern of patterns) {
            const match = driveLink.match(pattern);
            if (match && match[1]) return match[1];
            if (match && match[0]) return match[0];
        }
        return null;
    }
    
    function showResultMessage(directLink) {
        const resultMessage = document.createElement('div');
        resultMessage.className = 'chatbot-message result';
        resultMessage.innerHTML = `
            <p>Direct download link:</p>
            <p class="direct-link">${directLink}</p>
            <button class="copy-btn" data-link="${directLink}">
                <i class="fas fa-copy"></i> Copy Link
            </button>
        `;
        chatbotMessages.appendChild(resultMessage);
        scrollToBottom();
        
        resultMessage.querySelector('.copy-btn').addEventListener('click', function() {
            copyToClipboard(directLink, this);
        });
    }
    
    function copyToClipboard(text, button) {
        navigator.clipboard.writeText(text).then(() => {
            const originalHTML = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check"></i> Copied!';
            setTimeout(() => {
                button.innerHTML = originalHTML;
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy:', err);
            button.innerHTML = '<i class="fas fa-times"></i> Failed';
            setTimeout(() => {
                button.innerHTML = '<i class="fas fa-copy"></i> Copy Link';
            }, 2000);
        });
    }
    
    // Message helper functions
    function addBotMessage(text) {
        addMessage(text, 'bot');
    }
    
    function addUserMessage(text) {
        addMessage(text, 'user');
    }
    
    function addMessage(text, type) {
        const message = document.createElement('div');
        message.className = `chatbot-message ${type}`;
        message.innerHTML = `<p>${text}</p>`;
        chatbotMessages.appendChild(message);
        scrollToBottom();
    }
    
    function scrollToBottom() {
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
    
    // Event listeners for conversion
    convertBtn.addEventListener('click', function(e) {
        e.preventDefault();
        convertDriveLink();
    });
    
    driveLinkInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            convertDriveLink();
        }
    });
});