/**
 * Professional Dashboard - Kodbank
 * Refined fintech interface with subtle animations
 */

// Chart instance
let spendingChart = null;
let fireworksInterval = null;
let isFireworksActive = false;

document.addEventListener('DOMContentLoaded', () => {
    const accountOverviewCard = document.getElementById('accountOverviewCard');
    const sendMoneyBtn = document.getElementById('sendMoneyBtn');
    const balanceModal = document.getElementById('balanceModal');
    const closeBalanceModal = document.getElementById('closeBalanceModal');
    const transferModal = document.getElementById('transferModal');
    const closeModal = document.getElementById('closeModal');
    const transferForm = document.getElementById('transferForm');
    const balanceAmountEl = document.getElementById('balanceAmount');

    // Initialize chart
    initializeChart();

    // Load and display username
    loadUsername();

    // Account Overview Card Click - Show Balance Modal
    accountOverviewCard.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/balance', {
                method: 'GET',
                credentials: 'include'
            });

            const data = await response.json();
            console.log('Balance API Response:', data);

            if (response.ok && data.status === 'success') {
                console.log('Balance received:', data.balance);

                // Show modal
                balanceModal.classList.add('active');

                // Animate count-up
                animateCountUp(data.balance);

                // Trigger fireworks after count-up completes
                setTimeout(() => {
                    triggerRefinedCelebration();
                }, 1000);

                // Update other summary cards
                updateSummaryCards(data.balance);
            } else {
                if (response.status === 401) {
                    window.location.href = 'login.html';
                } else {
                    alert('Failed to retrieve balance');
                }
            }
        } catch (error) {
            console.error('Balance check error:', error);
            alert('Unable to connect to server');
        }
    });

    // Close Balance Modal
    closeBalanceModal.addEventListener('click', () => {
        balanceModal.classList.remove('active');
        stopFireworks();
    });

    // Close modal on outside click
    balanceModal.addEventListener('click', (e) => {
        if (e.target === balanceModal) {
            balanceModal.classList.remove('active');
            stopFireworks();
        }
    });

    // Open Transfer Modal
    sendMoneyBtn.addEventListener('click', () => {
        transferModal.classList.add('active');
    });

    // Close Transfer Modal
    closeModal.addEventListener('click', () => {
        transferModal.classList.remove('active');
        transferForm.reset();
        document.getElementById('transferMessage').style.display = 'none';
    });

    // Close modal on outside click
    transferModal.addEventListener('click', (e) => {
        if (e.target === transferModal) {
            transferModal.classList.remove('active');
            transferForm.reset();
            document.getElementById('transferMessage').style.display = 'none';
        }
    });

    // Handle Transfer Form
    transferForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const receiverUsername = document.getElementById('receiverUsername').value.trim();
        const amount = parseFloat(document.getElementById('amount').value);

        if (!receiverUsername) {
            showTransferMessage('Please enter receiver username', 'error');
            return;
        }

        if (isNaN(amount) || amount <= 0) {
            showTransferMessage('Please enter a valid amount greater than zero', 'error');
            return;
        }

        const submitBtn = transferForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';

        try {
            const response = await fetch('/api/transfer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    receiver_username: receiverUsername,
                    amount: amount
                })
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                showTransferMessage(
                    `${data.message}. Your new balance: ₹${data.sender_balance.toFixed(2)}`,
                    'success'
                );

                transferForm.reset();

                // Update balance
                document.getElementById('totalBalance').textContent = `₹${data.sender_balance.toFixed(2)}`;
                updateSummaryCards(data.sender_balance);

                // Reload transactions and activity
                loadTransactions();
                loadRecentActivity();

                // Close modal after 2 seconds
                setTimeout(() => {
                    transferModal.classList.remove('active');
                    document.getElementById('transferMessage').style.display = 'none';
                }, 2000);
            } else {
                if (response.status === 401) {
                    window.location.href = 'login.html';
                } else {
                    const errorMessage = data.message || 'Transfer failed. Please try again.';
                    showTransferMessage(errorMessage, 'error');
                }
            }
        } catch (error) {
            console.error('Transfer error:', error);
            showTransferMessage('Unable to connect to server. Please try again later.', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    });

    // Load initial data
    loadTransactions();
    loadRecentActivity();
    loadInitialBalance();
});

/**
 * Animate count-up effect for balance.
 */
function animateCountUp(finalValue) {
    const balanceAmountEl = document.getElementById('balanceAmount');
    
    if (!balanceAmountEl) {
        console.error('balanceAmount element not found!');
        return;
    }
    
    console.log('Starting count-up animation to:', finalValue);
    
    // Ensure the element is visible
    balanceAmountEl.style.display = 'inline';
    balanceAmountEl.style.color = '#000000';
    balanceAmountEl.style.fontSize = '48px';
    
    const duration = 800;
    const startTime = Date.now();
    const startValue = 0;

    function update() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Easing function
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const currentValue = startValue + (finalValue - startValue) * easeOutQuart;

        balanceAmountEl.textContent = currentValue.toFixed(2);
        console.log('Current balance display:', balanceAmountEl.textContent);

        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            console.log('Count-up animation complete. Final value:', balanceAmountEl.textContent);
        }
    }

    update();
}

/**
 * Trigger refined fireworks celebration animation.
 */
function triggerRefinedCelebration() {
    const celebrationContainer = document.getElementById('celebrationContainer');
    if (!celebrationContainer) return;

    // Stop any existing fireworks first
    stopFireworks();

    // Mark fireworks as active
    isFireworksActive = true;

    // Clear any existing fireworks
    celebrationContainer.innerHTML = '';

    const colors = [
        '#F59E0B', // Amber
        '#EF4444', // Red
        '#10B981', // Green
        '#3B82F6', // Blue
        '#8B5CF6', // Purple
        '#EC4899', // Pink
        '#F97316', // Orange
        '#14B8A6', // Teal
        '#F59E0B', // Amber (repeat for emphasis)
        '#FBBF24'  // Yellow
    ];

    const duration = 5000; // 5 seconds
    const startTime = Date.now();

    function createFirework() {
        if (!isFireworksActive) return;
        
        const now = Date.now();
        if (now - startTime > duration) return;

        // Random launch position (bottom of screen)
        const launchX = Math.random() * window.innerWidth;
        const launchY = window.innerHeight;

        // Random explosion position (upper half of screen)
        const explodeX = launchX + (Math.random() - 0.5) * 200;
        const explodeY = Math.random() * (window.innerHeight * 0.5);

        // Create rocket trail
        const rocket = document.createElement('div');
        rocket.style.position = 'fixed';
        rocket.style.left = launchX + 'px';
        rocket.style.top = launchY + 'px';
        rocket.style.width = '3px';
        rocket.style.height = '3px';
        rocket.style.borderRadius = '50%';
        rocket.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        rocket.style.boxShadow = '0 0 10px currentColor';
        rocket.style.pointerEvents = 'none';
        rocket.style.zIndex = '10000';
        celebrationContainer.appendChild(rocket);

        // Animate rocket
        const rocketDuration = 800 + Math.random() * 400;
        const rocketStart = Date.now();

        function animateRocket() {
            if (!isFireworksActive) {
                rocket.remove();
                return;
            }
            
            const elapsed = Date.now() - rocketStart;
            const progress = Math.min(elapsed / rocketDuration, 1);

            const currentX = launchX + (explodeX - launchX) * progress;
            const currentY = launchY - (launchY - explodeY) * progress;

            rocket.style.left = currentX + 'px';
            rocket.style.top = currentY + 'px';

            if (progress < 1) {
                requestAnimationFrame(animateRocket);
            } else {
                // Explosion
                rocket.remove();
                createExplosion(explodeX, explodeY);
            }
        }

        animateRocket();
    }

    function createExplosion(x, y) {
        if (!isFireworksActive) return;
        
        const particleCount = 80;
        const color = colors[Math.floor(Math.random() * colors.length)];

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.style.position = 'fixed';
            particle.style.left = x + 'px';
            particle.style.top = y + 'px';
            particle.style.width = '4px';
            particle.style.height = '4px';
            particle.style.borderRadius = '50%';
            particle.style.backgroundColor = color;
            particle.style.boxShadow = `0 0 6px ${color}`;
            particle.style.pointerEvents = 'none';
            particle.style.zIndex = '10000';
            celebrationContainer.appendChild(particle);

            // Random direction
            const angle = (Math.PI * 2 * i) / particleCount;
            const velocity = 2 + Math.random() * 4;
            const vx = Math.cos(angle) * velocity;
            const vy = Math.sin(angle) * velocity;

            const particleStart = Date.now();
            const particleDuration = 1500 + Math.random() * 500;

            function animateParticle() {
                if (!isFireworksActive) {
                    particle.remove();
                    return;
                }
                
                const elapsed = Date.now() - particleStart;
                const progress = elapsed / particleDuration;

                if (progress >= 1) {
                    particle.remove();
                    return;
                }

                const currentX = x + vx * elapsed * 0.1;
                const currentY = y + vy * elapsed * 0.1 + (0.5 * 0.002 * elapsed * elapsed * 0.01); // Gravity

                particle.style.left = currentX + 'px';
                particle.style.top = currentY + 'px';
                particle.style.opacity = 1 - progress;

                requestAnimationFrame(animateParticle);
            }

            animateParticle();
        }
    }

    // Launch fireworks at intervals
    fireworksInterval = setInterval(() => {
        if (!isFireworksActive || Date.now() - startTime > duration) {
            clearInterval(fireworksInterval);
            fireworksInterval = null;
            isFireworksActive = false;
            return;
        }
        createFirework();
    }, 300);

    // Launch initial burst
    createFirework();
    setTimeout(createFirework, 100);
    setTimeout(createFirework, 200);
}

/**
 * Stop fireworks animation and clear all particles.
 */
function stopFireworks() {
    isFireworksActive = false;
    
    if (fireworksInterval) {
        clearInterval(fireworksInterval);
        fireworksInterval = null;
    }
    
    const celebrationContainer = document.getElementById('celebrationContainer');
    if (celebrationContainer) {
        celebrationContainer.innerHTML = '';
    }
}

/**
 * Load initial balance on page load.
 */
async function loadInitialBalance() {
    try {
        const response = await fetch('/api/balance', {
            method: 'GET',
            credentials: 'include'
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
            // Don't update the Check Balance card - keep it hidden
            // Only update other summary cards
            const monthlyIncome = data.balance * 0.18;
            const monthlyExpenses = data.balance * 0.07;
            const totalSavings = data.balance * 0.27;
            
            document.getElementById('monthlyIncome').textContent = `₹${monthlyIncome.toFixed(2)}`;
            document.getElementById('monthlyExpenses').textContent = `₹${monthlyExpenses.toFixed(2)}`;
            document.getElementById('totalSavings').textContent = `₹${totalSavings.toFixed(2)}`;
        }
    } catch (error) {
        console.error('Error loading initial balance:', error);
    }
}

/**
 * Update summary cards with calculated values.
 */
function updateSummaryCards(balance) {
    const monthlyIncome = balance * 0.18;
    const monthlyExpenses = balance * 0.07;
    const totalSavings = balance * 0.27;

    document.getElementById('monthlyIncome').textContent = `₹${monthlyIncome.toFixed(2)}`;
    document.getElementById('monthlyExpenses').textContent = `₹${monthlyExpenses.toFixed(2)}`;
    document.getElementById('totalSavings').textContent = `₹${totalSavings.toFixed(2)}`;
}

/**
 * Initialize spending chart with refined styling.
 */
function initializeChart() {
    const canvas = document.getElementById('spendingChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const spending = [450, 320, 580, 290, 610, 380, 520];

    const padding = 40;
    const width = canvas.width;
    const height = canvas.height;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;

    const maxSpending = Math.max(...spending);
    const scale = chartHeight / maxSpending;

    ctx.clearRect(0, 0, width, height);

    // Draw minimal grid lines (5% opacity)
    ctx.strokeStyle = 'rgba(229, 231, 235, 0.05)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
        const y = padding + (chartHeight / 5) * i;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
    }

    // Draw gradient area
    const gradient = ctx.createLinearGradient(0, padding, 0, height - padding);
    gradient.addColorStop(0, 'rgba(245, 158, 11, 0.15)');
    gradient.addColorStop(1, 'rgba(245, 158, 11, 0.0)');

    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.moveTo(padding, height - padding);

    spending.forEach((value, index) => {
        const x = padding + (chartWidth / (days.length - 1)) * index;
        const y = height - padding - (value * scale);
        ctx.lineTo(x, y);
    });

    ctx.lineTo(width - padding, height - padding);
    ctx.closePath();
    ctx.fill();

    // Draw line with soft glow
    ctx.strokeStyle = '#F59E0B';
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.shadowBlur = 8;
    ctx.shadowColor = 'rgba(245, 158, 11, 0.3)';

    ctx.beginPath();
    spending.forEach((value, index) => {
        const x = padding + (chartWidth / (days.length - 1)) * index;
        const y = height - padding - (value * scale);
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    ctx.stroke();

    // Draw points
    ctx.shadowBlur = 0;
    spending.forEach((value, index) => {
        const x = padding + (chartWidth / (days.length - 1)) * index;
        const y = height - padding - (value * scale);

        ctx.fillStyle = '#F59E0B';
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#141A22';
        ctx.beginPath();
        ctx.arc(x, y, 2, 0, Math.PI * 2);
        ctx.fill();
    });

    // Draw labels
    ctx.fillStyle = '#9CA3AF';
    ctx.font = '11px Inter, sans-serif';
    ctx.textAlign = 'center';

    days.forEach((day, index) => {
        const x = padding + (chartWidth / (days.length - 1)) * index;
        ctx.fillText(day, x, height - padding + 20);
    });
}

/**
 * Load recent activity (top 5 transactions).
 */
async function loadRecentActivity() {
    const container = document.getElementById('recentActivityContainer');

    try {
        const response = await fetch('/api/transactions?limit=5', {
            method: 'GET',
            credentials: 'include'
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
            const transactions = data.transactions;

            if (transactions.length === 0) {
                container.innerHTML = '<p class="no-transactions">No recent activity</p>';
                return;
            }

            let listHTML = '<div class="activity-list">';

            transactions.forEach(transaction => {
                const date = new Date(transaction.created_at);
                const formattedDate = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                const formattedTime = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

                const isSent = transaction.direction === 'sent';
                const otherParty = isSent ? transaction.receiver_username : transaction.sender_username;
                const amountClass = isSent ? 'debit' : 'credit';
                const amountPrefix = isSent ? '-' : '+';
                const iconClass = isSent ? 'debit' : 'credit';

                const icon = isSent ?
                    '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 10.5L12 3m0 0l7.5 7.5M12 3v18" /></svg>' :
                    '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 13.5L12 21m0 0l-7.5-7.5M12 21V3" /></svg>';

                listHTML += `
                    <div class="activity-item">
                        <div class="activity-icon ${iconClass}">
                            ${icon}
                        </div>
                        <div class="activity-details">
                            <p class="activity-name">${otherParty}</p>
                            <p class="activity-meta">${formattedDate} • ${formattedTime}</p>
                        </div>
                        <div class="activity-amount-wrapper">
                            <span class="activity-amount ${amountClass}">${amountPrefix}₹${transaction.amount.toFixed(2)}</span>
                            <span class="activity-status completed">Completed</span>
                        </div>
                    </div>
                `;
            });

            listHTML += '</div>';
            container.innerHTML = listHTML;
        } else {
            if (response.status === 401) {
                window.location.href = 'login.html';
            } else {
                container.innerHTML = '<p class="error-message">Failed to load activity</p>';
            }
        }
    } catch (error) {
        console.error('Error loading activity:', error);
        container.innerHTML = '<p class="error-message">Unable to load activity</p>';
    }
}

/**
 * Load transaction history.
 */
async function loadTransactions() {
    const transactionsContainer = document.getElementById('transactionsContainer');

    try {
        const response = await fetch('/api/transactions?limit=10', {
            method: 'GET',
            credentials: 'include'
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
            const transactions = data.transactions;

            if (transactions.length === 0) {
                transactionsContainer.innerHTML = '<p class="no-transactions">No transactions yet</p>';
                updateStats([], 0, 0, 0);
                return;
            }

            let totalSent = 0;
            let totalReceived = 0;

            transactions.forEach(transaction => {
                if (transaction.direction === 'sent') {
                    totalSent += transaction.amount;
                } else {
                    totalReceived += transaction.amount;
                }
            });

            updateStats(transactions, totalSent, totalReceived, transactions.length);

            let listHTML = '<div class="transactions-list">';

            transactions.forEach(transaction => {
                const date = new Date(transaction.created_at);
                const formattedDate = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

                const isSent = transaction.direction === 'sent';
                const otherParty = isSent ? transaction.receiver_username : transaction.sender_username;
                const amountClass = isSent ? 'negative' : 'positive';
                const amountPrefix = isSent ? '-' : '+';
                const iconClass = isSent ? 'sent' : 'received';

                const icon = isSent ?
                    '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 10.5L12 3m0 0l7.5 7.5M12 3v18" /></svg>' :
                    '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 13.5L12 21m0 0l-7.5-7.5M12 21V3" /></svg>';

                listHTML += `
                    <div class="transaction-item">
                        <div class="transaction-icon ${iconClass}">
                            ${icon}
                        </div>
                        <div class="transaction-details">
                            <p class="transaction-merchant">${otherParty}</p>
                            <p class="transaction-meta">${formattedDate}</p>
                        </div>
                        <div class="transaction-amount-wrapper">
                            <span class="transaction-amount ${amountClass}">${amountPrefix}₹${transaction.amount.toFixed(2)}</span>
                            <span class="transaction-status completed">Completed</span>
                        </div>
                    </div>
                `;
            });

            listHTML += '</div>';
            transactionsContainer.innerHTML = listHTML;
        } else {
            if (response.status === 401) {
                window.location.href = 'login.html';
            } else {
                transactionsContainer.innerHTML = '<p class="error-message">Failed to load transactions</p>';
            }
        }
    } catch (error) {
        console.error('Error loading transactions:', error);
        transactionsContainer.innerHTML = '<p class="error-message">Unable to load transactions</p>';
    }
}

/**
 * Update quick stats display.
 */
function updateStats(transactions, totalSent, totalReceived, count) {
    const totalSentEl = document.getElementById('totalSent');
    const totalReceivedEl = document.getElementById('totalReceived');
    const transactionCountEl = document.getElementById('transactionCount');

    if (totalSentEl) totalSentEl.textContent = `₹${totalSent.toFixed(2)}`;
    if (totalReceivedEl) totalReceivedEl.textContent = `₹${totalReceived.toFixed(2)}`;
    if (transactionCountEl) transactionCountEl.textContent = count;
}

/**
 * Display transfer message to user.
 */
function showTransferMessage(message, type) {
    const transferMessage = document.getElementById('transferMessage');
    if (transferMessage) {
        transferMessage.textContent = message;
        transferMessage.className = `message ${type}`;
        transferMessage.style.display = 'block';

        if (type === 'success') {
            setTimeout(() => {
                transferMessage.style.display = 'none';
            }, 5000);
        }
    }
}


/**
 * Load and display the logged-in username.
 */
async function loadUsername() {
    try {
        const response = await fetch('/api/balance', {
            method: 'GET',
            credentials: 'include'
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
            // Extract username from the JWT token by making another API call
            // Or we can modify the balance endpoint to return username
            // For now, let's get it from localStorage if stored during login
            const username = localStorage.getItem('username');
            if (username) {
                document.getElementById('username').textContent = username;
            }
        }
    } catch (error) {
        console.error('Error loading username:', error);
    }
}
