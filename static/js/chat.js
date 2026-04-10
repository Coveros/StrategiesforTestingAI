// Chat Application JavaScript
class ChatApp {
    constructor() {
        this.isLoading = false;
        this.messageHistory = [];
        this.apiEndpoint = '/api/chat';
        this.statsEndpoint = '/api/stats';
        this.healthEndpoint = '/api/health';
        this.appFlags = window.APP_FLAGS || {};
        this.queryParams = new URLSearchParams(window.location.search);
        this.instructorMode = Boolean(this.appFlags.instructorMode) || this.queryParams.get('instructor') === '1';
        this.exerciseNumber = Number(this.queryParams.get('exercise') || 0);
        this.modeStorageKey = 'chatPreferredMode';
        this.canUseAgentMode = true;
        this.sessionId = localStorage.getItem('chatSessionId') || `session-${Date.now()}`;
        localStorage.setItem('chatSessionId', this.sessionId);
        
        this.initializeElements();
        this.initializeInstructorControls();
        this.initializeModeSwitch();
        this.setupEventListeners();
        this.checkSystemHealth();
        
        // Auto-resize textarea
        this.setupAutoResize();
        
        console.log('GenAI Testing Tutorial Chat App initialized');
    }
    
    initializeElements() {
        // Core elements
        this.messagesContainer = document.getElementById('messagesContainer');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatForm = document.getElementById('chatForm');
        this.characterCount = document.getElementById('characterCount');
        
        // Header elements
        this.statusIndicator = document.getElementById('statusIndicator');
        this.clearChatButton = document.getElementById('clearChat');
        this.showStatsButton = document.getElementById('showStats');
        this.instructorControls = document.getElementById('instructorControls');
        this.tempOverrideEnabled = document.getElementById('tempOverrideEnabled');
        this.temperatureInput = document.getElementById('temperatureInput');
        this.agentModeEnabled = document.getElementById('agentModeEnabled');
        this.showTraceEnabled = document.getElementById('showTraceEnabled');
        this.crewModeEnabled = document.getElementById('crewModeEnabled');
        this.askModeBtn = document.getElementById('askModeBtn');
        this.agentModeBtn = document.getElementById('agentModeBtn');
        this.modeTemperature = document.getElementById('modeTemperature');
        this.modeHint = document.getElementById('modeHint');
        
        // Modal elements
        this.statsModal = document.getElementById('statsModal');
        this.statsContent = document.getElementById('statsContent');
        this.closeStatsButton = document.getElementById('closeStats');
        
        // Toast elements
        this.errorToast = document.getElementById('errorToast');
    }

    initializeInstructorControls() {
        if (
            !this.instructorControls ||
            !this.tempOverrideEnabled ||
            !this.temperatureInput ||
            !this.agentModeEnabled ||
            !this.showTraceEnabled ||
            !this.crewModeEnabled
        ) {
            return;
        }

        if (!this.instructorMode) {
            this.instructorControls.style.display = 'none';
            return;
        }

        this.instructorControls.style.display = 'flex';

        const savedEnabled = localStorage.getItem('instructorTempEnabled');
        const savedTemp = localStorage.getItem('instructorTempValue');
        const savedAgentMode = localStorage.getItem('instructorAgentModeEnabled');
        const savedTraceMode = localStorage.getItem('instructorShowTraceEnabled');
        const savedCrewMode = localStorage.getItem('instructorCrewModeEnabled');

        this.tempOverrideEnabled.checked = savedEnabled === 'true';
        if (savedTemp !== null && savedTemp !== '') {
            this.temperatureInput.value = savedTemp;
        }
        this.agentModeEnabled.checked = savedAgentMode === 'true';
        this.showTraceEnabled.checked = savedTraceMode === 'true';
        this.crewModeEnabled.checked = savedCrewMode === 'true';

        this.updateInstructorTemperatureState();
    }

    initializeModeSwitch() {
        if (!this.askModeBtn || !this.agentModeBtn) {
            this.activeMode = 'ask';
            return;
        }

        const saved = localStorage.getItem(this.modeStorageKey);
        const queryWantsAgent = this.queryParams.get('agent') === '1';
        const defaultByExercise = this.exerciseNumber >= 5;
        const initialMode = saved || (queryWantsAgent || defaultByExercise ? 'agent' : 'ask');
        this.setChatMode(initialMode, false);

        this.askModeBtn.addEventListener('click', () => this.setChatMode('ask', true));
        this.agentModeBtn.addEventListener('click', () => this.setChatMode('agent', true));

        if (this.modeTemperature) {
            const savedTemp = localStorage.getItem('chatModeTemperature');
            if (savedTemp !== null && savedTemp !== '') {
                this.modeTemperature.value = this.normalizeTemperatureValue(savedTemp).toFixed(1);
            }
            this.modeTemperature.addEventListener('change', () => {
                const value = this.normalizeTemperatureValue(this.modeTemperature.value);
                this.modeTemperature.value = value.toFixed(1);
                localStorage.setItem('chatModeTemperature', String(value));
            });
        }
    }

    setChatMode(mode, persist) {
        this.activeMode = mode === 'agent' ? 'agent' : 'ask';
        if (persist) {
            localStorage.setItem(this.modeStorageKey, this.activeMode);
        }

        if (this.askModeBtn && this.agentModeBtn) {
            const askActive = this.activeMode === 'ask';
            this.askModeBtn.classList.toggle('active', askActive);
            this.agentModeBtn.classList.toggle('active', !askActive);
            this.askModeBtn.setAttribute('aria-pressed', askActive ? 'true' : 'false');
            this.agentModeBtn.setAttribute('aria-pressed', askActive ? 'false' : 'true');
        }

        if (this.instructorMode && this.agentModeEnabled) {
            this.agentModeEnabled.checked = this.activeMode === 'agent';
            this.updateInstructorTemperatureState();
        }

        this.updateModeHint();
    }

    getExerciseDefaults() {
        return {
            trace: this.exerciseNumber >= 6,
            crew: this.exerciseNumber >= 8,
        };
    }

    updateModeHint() {
        if (!this.modeHint) {
            return;
        }

        if (this.activeMode !== 'agent') {
            this.modeHint.textContent = 'Ask mode: temperature is applied to RAG responses.';
            return;
        }

        const defaults = this.getExerciseDefaults();
        if (defaults.crew) {
            this.modeHint.textContent = 'Agent mode: trace and crew are auto-enabled for this exercise.';
            return;
        }

        if (defaults.trace) {
            this.modeHint.textContent = 'Agent mode: trace is auto-enabled for this exercise.';
            return;
        }

        this.modeHint.textContent = 'Agent mode: baseline agent flow (trace and crew off by default).';
    }
    
    setupEventListeners() {
        // Form submission
        this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Input events
        this.messageInput.addEventListener('input', () => this.updateCharacterCount());
        this.messageInput.addEventListener('keydown', (e) => this.handleKeyDown(e));
        
        // Header actions
        this.clearChatButton.addEventListener('click', () => this.clearChat());
        this.showStatsButton.addEventListener('click', () => this.showStats());

        if (this.instructorMode && this.tempOverrideEnabled && this.temperatureInput) {
            this.tempOverrideEnabled.addEventListener('change', () => {
                localStorage.setItem('instructorTempEnabled', String(this.tempOverrideEnabled.checked));
                this.updateInstructorTemperatureState();
            });

            this.temperatureInput.addEventListener('change', () => {
                const value = this.normalizeTemperatureValue(this.temperatureInput.value);
                this.temperatureInput.value = value.toFixed(1);
                localStorage.setItem('instructorTempValue', String(value));
            });

            this.agentModeEnabled.addEventListener('change', () => {
                if (this.instructorMode) {
                    localStorage.setItem('instructorAgentModeEnabled', String(this.agentModeEnabled.checked));
                }
                this.setChatMode(this.agentModeEnabled.checked ? 'agent' : 'ask', true);
                this.updateInstructorTemperatureState();
            });

            this.showTraceEnabled.addEventListener('change', () => {
                localStorage.setItem('instructorShowTraceEnabled', String(this.showTraceEnabled.checked));
            });

            this.crewModeEnabled.addEventListener('change', () => {
                localStorage.setItem('instructorCrewModeEnabled', String(this.crewModeEnabled.checked));
            });
        }
        
        // Modal events
        this.closeStatsButton.addEventListener('click', () => this.closeStats());
        this.statsModal.addEventListener('click', (e) => {
            if (e.target === this.statsModal) this.closeStats();
        });
        
        // Example questions
        this.setupExampleQuestions();
        
        // Toast close
        const toastClose = this.errorToast.querySelector('.toast-close');
        if (toastClose) {
            toastClose.addEventListener('click', () => this.hideToast());
        }
        
        // Auto-hide toast after 5 seconds
        setTimeout(() => this.hideToast(), 5000);
    }
    
    setupExampleQuestions() {
        const exampleQuestions = document.querySelectorAll('.example-questions li');
        exampleQuestions.forEach(item => {
            item.addEventListener('click', () => {
                const question = item.textContent.replace(/^💬\s*"?/, '').replace(/"$/, '');
                this.messageInput.value = question;
                this.updateCharacterCount();
                this.messageInput.focus();
            });
        });
    }
    
    setupAutoResize() {
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
        });
    }
    
    updateCharacterCount() {
        const count = this.messageInput.value.length;
        const maxLength = 1000;
        
        this.characterCount.textContent = `${count}/${maxLength}`;
        
        // Update styling based on count
        this.characterCount.className = 'character-count';
        if (count > maxLength * 0.9) {
            this.characterCount.classList.add('warning');
        }
        if (count >= maxLength) {
            this.characterCount.classList.add('error');
        }
    }
    
    handleKeyDown(e) {
        // Send message with Ctrl+Enter or Cmd+Enter
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (!this.isLoading && this.messageInput.value.trim()) {
                this.handleSubmit(e);
            }
        }
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        const message = this.messageInput.value.trim();
        if (!message || this.isLoading) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input and show loading
        this.messageInput.value = '';
        this.updateCharacterCount();
        this.setLoading(true);
        
        // Show typing indicator
        const typingId = this.showTypingIndicator();
        
        try {
            const requestPayload = { message: message };
            requestPayload.session_id = this.sessionId;

            if (this.getAgentModeEnabled()) {
                requestPayload.mode = 'agentic';
                requestPayload.include_trace = this.getTraceEnabled();
                requestPayload.crew_mode = this.getCrewModeEnabled();
            } else {
                requestPayload.mode = 'rag';
            }

            const selectedTemperature = this.getSelectedTemperature();
            if (selectedTemperature !== null) {
                requestPayload.temperature = selectedTemperature;
            }

            // Send request to API
            const response = await fetch(this.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestPayload)
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            this.removeTypingIndicator(typingId);
            
            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}`);
            }
            
            // Add assistant response
            this.addMessage(data.response, 'assistant', {
                sources: data.sources,
                responseTime: data.response_time,
                retrievalTime: data.retrieval_time,
                generationTime: data.generation_time,
                temperature: data.temperature,
                mode: data.mode,
                toolCalls: data.tool_calls,
                agentTrace: data.agent_trace,
                stateSnapshot: data.state_snapshot,
                handoffs: data.handoffs,
                trajectoryMetrics: data.trajectory_metrics,
                crewMode: data.crew_mode
            });
            
            // Store in history
            this.messageHistory.push({
                user: message,
                assistant: data.response,
                timestamp: Date.now(),
                metadata: data
            });
            
        } catch (error) {
            console.error('Error sending message:', error);
            
            // Remove typing indicator
            this.removeTypingIndicator(typingId);
            
            // Show error message
            this.addMessage(
                `I apologize, but I encountered an error: ${error.message}. Please try again.`,
                'assistant',
                { error: true }
            );
            
            // Show error toast
            this.showErrorToast(`Failed to send message: ${error.message}`);
        } finally {
            this.setLoading(false);
        }
    }
    
    addMessage(content, type, metadata = {}) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        messageElement.innerHTML = this.createMessageHTML(content, type, metadata);
        
        // Remove welcome message if it exists
        const welcomeMessage = this.messagesContainer.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }
        
        this.messagesContainer.appendChild(messageElement);
        this.scrollToBottom();
    }
    
    createMessageHTML(content, type, metadata) {
        const timestamp = new Date().toLocaleTimeString();
        const avatar = type === 'user' ? '👤' : '🤖';
        
        let sourcesHTML = '';
        if (metadata.sources && metadata.sources.length > 0) {
            const sourceItems = metadata.sources.map(source => `
                <div class="source-item">
                    <div class="source-header">
                        <div class="source-title">📄 ${source.metadata && source.metadata.source ? source.metadata.source : 'Unknown Document'}</div>
                        <div class="source-similarity">Similarity: ${source.similarity}%</div>
                    </div>
                    <div class="source-content">${this.escapeHtml(source.content)}</div>
                </div>
            `).join('');
            
            sourcesHTML = `
                <div class="message-sources">
                    <div class="sources-header">📚 Sources (${metadata.sources.length}):</div>
                    ${sourceItems}
                </div>
            `;
        }
        
        let metaInfo = timestamp;
        if (metadata.responseTime) {
            metaInfo += ` • ${(metadata.responseTime * 1000).toFixed(0)}ms`;
        }
        if (metadata.temperature !== undefined && metadata.temperature !== null) {
            metaInfo += ` • temp ${Number(metadata.temperature).toFixed(2)}`;
        }
        if (metadata.mode) {
            metaInfo += ` • ${metadata.mode}`;
        }
        if (metadata.crewMode) {
            metaInfo += ' • crew';
        }
        if (metadata.error) {
            metaInfo += ' • Error';
        }

        let agentBlock = '';
        if ((metadata.toolCalls && metadata.toolCalls.length > 0) || (metadata.agentTrace && metadata.agentTrace.length > 0)) {
            const tools = (metadata.toolCalls || []).map((call, idx) => {
                const details = [];
                if (call.scope) details.push(`scope=${call.scope}`);
                if (call.test_id) details.push(`test_id=${call.test_id}`);
                if (call.severity) details.push(`severity=${call.severity}`);
                return `<li><strong>${idx + 1}. ${call.tool}</strong>${details.length ? ` (${details.join(', ')})` : ''}</li>`;
            }).join('');

            const trace = (metadata.agentTrace || []).map((step, idx) =>
                `<li><strong>${idx + 1}. ${step.phase}</strong>: ${this.escapeHtml(step.content)}</li>`
            ).join('');

            const stateSummary = metadata.stateSnapshot && metadata.stateSnapshot.tracked_failure
                ? `Tracked Failure: ${this.escapeHtml(metadata.stateSnapshot.tracked_failure)}`
                : 'Tracked Failure: none';

            const handoffs = (metadata.handoffs || []).map((h, idx) =>
                `<li><strong>${idx + 1}. ${this.escapeHtml(h.from)} -> ${this.escapeHtml(h.to)}</strong>: ${this.escapeHtml(h.purpose || '')}</li>`
            ).join('');

            const metrics = metadata.trajectoryMetrics || {};
            const metricsLine = `steps=${metrics.steps || 0}, tools=${metrics.tool_calls || 0}, handoffs=${metrics.handoffs || 0}, redundant=${metrics.redundant_tool_calls || 0}`;

            agentBlock = `
                <div class="agent-debug-block">
                    <div class="agent-debug-header">Agent Execution</div>
                    <div class="agent-debug-state">${stateSummary}</div>
                    <div class="agent-debug-state">Trajectory: ${metricsLine}</div>
                    ${tools ? `<div class="agent-debug-section"><div class="agent-debug-label">Tools Called</div><ol>${tools}</ol></div>` : ''}
                    ${handoffs ? `<div class="agent-debug-section"><div class="agent-debug-label">Handoffs</div><ol>${handoffs}</ol></div>` : ''}
                    ${trace ? `<div class="agent-debug-section"><div class="agent-debug-label">Trace</div><ol>${trace}</ol></div>` : ''}
                </div>
            `;
        }
        
        return `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <div class="message-bubble">
                    ${this.formatMessageContent(content)}
                    ${sourcesHTML}
                    ${agentBlock}
                </div>
                <div class="message-meta">
                    <span>${metaInfo}</span>
                </div>
            </div>
        `;
    }
    
    formatMessageContent(content) {
        // Basic formatting for better readability
        return this.escapeHtml(content)
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>');
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    showTypingIndicator() {
        const typingId = `typing-${Date.now()}`;
        const typingElement = document.createElement('div');
        typingElement.className = 'message assistant';
        typingElement.id = typingId;
        typingElement.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <div class="message-bubble">
                    <div class="typing-indicator">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            </div>
        `;
        
        this.messagesContainer.appendChild(typingElement);
        this.scrollToBottom();
        
        return typingId;
    }
    
    removeTypingIndicator(typingId) {
        const typingElement = document.getElementById(typingId);
        if (typingElement) {
            typingElement.remove();
        }
    }
    
    setLoading(loading) {
        this.isLoading = loading;
        
        const buttonText = this.sendButton.querySelector('.button-text');
        const loadingSpinner = this.sendButton.querySelector('.loading-spinner');
        
        if (loading) {
            buttonText.style.display = 'none';
            loadingSpinner.style.display = 'flex';
            this.sendButton.disabled = true;
            this.messageInput.disabled = true;
        } else {
            buttonText.style.display = 'inline';
            loadingSpinner.style.display = 'none';
            this.sendButton.disabled = false;
            this.messageInput.disabled = false;
            this.messageInput.focus();
        }
    }
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    clearChat() {
        // Remove all messages except welcome
        const messages = this.messagesContainer.querySelectorAll('.message');
        messages.forEach(message => message.remove());
        
        // Reset message history
        this.messageHistory = [];
        
        // Show welcome message again if it doesn't exist
        if (!this.messagesContainer.querySelector('.welcome-message')) {
            location.reload(); // Simple way to restore welcome message
        }
        
        console.log('Chat cleared');
    }
    
    async showStats() {
        this.statsModal.style.display = 'block';
        this.statsContent.innerHTML = '<div class="loading">Loading statistics...</div>';
        
        try {
            // Fetch system stats
            const response = await fetch(this.statsEndpoint);
            const stats = await response.json();
            
            // Fetch health status
            const healthResponse = await fetch(this.healthEndpoint);
            const health = await healthResponse.json();
            
            this.renderStats(stats, health);
            
        } catch (error) {
            console.error('Error fetching stats:', error);
            this.statsContent.innerHTML = `
                <div class="error">
                    <p>Failed to load statistics: ${error.message}</p>
                </div>
            `;
        }
    }
    
    renderStats(stats, health) {
        const agentic = stats.agentic || {};
        const statsHTML = `
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">${stats.queries_processed || 0}</div>
                    <div class="stat-label">Queries Processed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.average_response_time || 0}s</div>
                    <div class="stat-label">Avg Response Time</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.documents_loaded || 0}</div>
                    <div class="stat-label">Documents Loaded</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${((stats.error_rate || 0) * 100).toFixed(1)}%</div>
                    <div class="stat-label">Error Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${agentic.tool_calls || 0}</div>
                    <div class="stat-label">Agent Tool Calls</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${agentic.blocked_actions || 0}</div>
                    <div class="stat-label">Blocked Actions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${agentic.crew_requests || 0}</div>
                    <div class="stat-label">Crew Requests</div>
                </div>
            </div>
            
            <div class="health-check">
                <h4 style="margin-bottom: 12px; color: #374151;">System Health</h4>
                <div class="health-item">
                    <span>Cohere API</span>
                    <span class="health-status ${health.cohere_client ? 'healthy' : 'unhealthy'}">
                        ${health.cohere_client ? 'Connected' : 'Disconnected'}
                    </span>
                </div>
                <div class="health-item">
                    <span>Vector Database</span>
                    <span class="health-status ${health.vector_db ? 'healthy' : 'unhealthy'}">
                        ${health.vector_db ? 'Connected' : 'Disconnected'}
                    </span>
                </div>
                <div class="health-item">
                    <span>Document Collection</span>
                    <span class="health-status ${health.collection ? 'healthy' : 'unhealthy'}">
                        ${health.collection ? 'Ready' : 'Not Ready'}
                    </span>
                </div>
                <div class="health-item">
                    <span>Knowledge Base</span>
                    <span class="health-status ${health.documents_loaded ? 'healthy' : 'unhealthy'}">
                        ${health.documents_loaded ? 'Loaded' : 'Empty'}
                    </span>
                </div>
            </div>
            
            <div style="margin-top: 20px; padding-top: 16px; border-top: 1px solid #e5e7eb; font-size: 0.8rem; color: #6b7280;">
                <p><strong>Session Info:</strong> ${this.messageHistory.length} messages in history</p>
                <p><strong>Last Updated:</strong> ${new Date().toLocaleString()}</p>
            </div>
        `;
        
        this.statsContent.innerHTML = statsHTML;
    }
    
    closeStats() {
        this.statsModal.style.display = 'none';
    }
    
    async checkSystemHealth() {
        try {
            const response = await fetch(this.healthEndpoint);
            const health = await response.json();
            
            this.updateStatusIndicator(health);
            
        } catch (error) {
            console.error('Health check failed:', error);
            this.updateStatusIndicator({ status: 'unhealthy' });
        }
    }
    
    updateStatusIndicator(health) {
        const statusDot = this.statusIndicator.querySelector('.status-dot');
        const statusText = this.statusIndicator.querySelector('span');
        
        if (health.status === 'healthy') {
            statusDot.className = 'status-dot connected';
            statusText.textContent = 'Connected';
        } else {
            statusDot.className = 'status-dot error';
            statusText.textContent = 'Connection Issues';
        }
    }
    
    showErrorToast(message) {
        const toastMessage = this.errorToast.querySelector('.toast-message');
        toastMessage.textContent = message;
        
        this.errorToast.classList.add('show');
        
        // Auto-hide after 5 seconds
        setTimeout(() => this.hideToast(), 5000);
    }
    
    hideToast() {
        this.errorToast.classList.remove('show');
    }

    updateInstructorTemperatureState() {
        if (!this.temperatureInput || !this.tempOverrideEnabled || !this.agentModeEnabled || !this.showTraceEnabled || !this.crewModeEnabled) {
            return;
        }

        const agentModeActive = this.agentModeEnabled.checked;

        this.temperatureInput.disabled = !this.tempOverrideEnabled.checked || agentModeActive;
        this.temperatureInput.style.opacity = this.temperatureInput.disabled ? '0.6' : '1';

        this.showTraceEnabled.disabled = !agentModeActive;
        this.showTraceEnabled.style.opacity = agentModeActive ? '1' : '0.6';

        if (!agentModeActive) {
            this.showTraceEnabled.checked = false;
            this.crewModeEnabled.checked = false;
            localStorage.setItem('instructorShowTraceEnabled', 'false');
            localStorage.setItem('instructorCrewModeEnabled', 'false');
        }

        this.crewModeEnabled.disabled = !agentModeActive;
        this.crewModeEnabled.style.opacity = agentModeActive ? '1' : '0.6';
    }

    normalizeTemperatureValue(rawValue) {
        const parsed = Number(rawValue);
        if (Number.isNaN(parsed)) {
            return 0.7;
        }
        return Math.max(0, Math.min(1, parsed));
    }

    getSelectedTemperature() {
        if (this.getAgentModeEnabled()) {
            return null;
        }

        if (this.instructorMode && this.tempOverrideEnabled && this.temperatureInput && this.tempOverrideEnabled.checked) {
            const normalizedInstructor = this.normalizeTemperatureValue(this.temperatureInput.value);
            this.temperatureInput.value = normalizedInstructor.toFixed(1);
            localStorage.setItem('instructorTempValue', String(normalizedInstructor));
            return normalizedInstructor;
        }

        if (!this.modeTemperature) {
            return null;
        }

        const normalized = this.normalizeTemperatureValue(this.modeTemperature.value);
        this.modeTemperature.value = normalized.toFixed(1);
        localStorage.setItem('chatModeTemperature', String(normalized));
        return normalized;
    }

    getAgentModeEnabled() {
        if (!this.canUseAgentMode) {
            return false;
        }
        return this.activeMode === 'agent';
    }

    getTraceEnabled() {
        if (!this.getAgentModeEnabled()) {
            return false;
        }

        if (this.instructorMode) {
            return Boolean(this.showTraceEnabled && this.showTraceEnabled.checked);
        }

        return this.getExerciseDefaults().trace;
    }

    getCrewModeEnabled() {
        if (!this.getAgentModeEnabled()) {
            return false;
        }

        if (this.instructorMode) {
            return Boolean(this.crewModeEnabled && this.crewModeEnabled.checked);
        }

        return this.getExerciseDefaults().crew;
    }
}

// Initialize the chat app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.chatApp = new ChatApp();
});

// Export for potential testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChatApp;
}