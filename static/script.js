// 로그인 폼 제출 이벤트
document.getElementById('loginForm')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const id = document.getElementById('loginId').value;
    const password = document.getElementById('loginPassword').value;

    if (id === 'user' && password === 'password') {
        window.location.href = 'index.html';
    } else {
        document.getElementById('loginError').innerText = '일치하지 않습니다!';
    }
});

// ID 가용성 확인 함수
function checkIdAvailability() {
    const id = document.getElementById('createId').value;

    if (id !== 'user') {
        alert('ID is available');
    } else {
        alert('ID is already taken');
    }
}

// 계정 생성 폼 제출 이벤트
document.getElementById('createAccountForm')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const id = document.getElementById('createId').value;
    const password = document.getElementById('createPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password === confirmPassword && id !== 'user') {
        alert('Account created successfully');
        window.location.href = 'index.html';
    } else {
        document.getElementById('createError').innerText = '계정 생성 실패';
    }
});

// 다크 모드 토글 스위치 이벤트
document.getElementById('themeSwitch')?.addEventListener('change', function() {
    if (this.checked) {
        enableDarkMode();
    } else {
        disableDarkMode();
    }
});

function enableDarkMode() {
    document.body.classList.add('dark-mode');
    document.querySelector('.container').classList.add('dark-mode');
    document.querySelectorAll('button').forEach(button => button.classList.add('dark-mode'));
    document.querySelectorAll('a').forEach(link => link.classList.add('dark-mode'));
    document.querySelectorAll('h1').forEach(title => title.classList.add('dark-mode'));
    document.querySelectorAll('h2').forEach(subtitle => subtitle.classList.add('dark-mode'));
    localStorage.setItem('theme', 'dark');
}

function disableDarkMode() {
    document.body.classList.remove('dark-mode');
    document.querySelector('.container').classList.remove('dark-mode');
    document.querySelectorAll('button').forEach(button => button.classList.remove('dark-mode'));
    document.querySelectorAll('a').forEach(link => link.classList.remove('dark-mode'));
    document.querySelectorAll('h1').forEach(title => title.classList.remove('dark-mode'));
    document.querySelectorAll('h2').forEach(subtitle => subtitle.classList.remove('dark-mode'));
    localStorage.setItem('theme', 'light');
}

// 페이지 로드 시 저장된 테마 적용
document.addEventListener('DOMContentLoaded', function() {
    const theme = localStorage.getItem('theme');
    if (theme === 'dark') {
        enableDarkMode();
        document.getElementById('themeSwitch').checked = true;
    } else {
        disableDarkMode();
    }
});

// HTML 요소들과 상호작용
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatOutput = document.getElementById('chatOutput');

    chatForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const userMessage = chatInput.value;
        chatOutput.innerHTML += `<p><strong>You:</strong> ${userMessage}</p>`;

        try {
            const response = await fetch('https://api.openai.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer YOURKEY`
                },
                body: JSON.stringify({
                    model: "gpt-4o",
                    messages: [
                        { role: "system", content: "You are a delivery arrival notification chatbot service system. You output appropriate messages based on the user's questions. You answer in a language that matches the language the user wrote." },
                        { role: "user", content: userMessage }
                    ],
                    temperature: 1,
                    max_tokens: 256,
                    top_p: 1,
                    frequency_penalty: 0,
                    presence_penalty: 0,
                })
            });

            const data = await response.json();
            const botMessage = data.choices[0].message.content;
            chatOutput.innerHTML += `<p><strong>Bot:</strong> ${botMessage}</p>`;
        } catch (error) {
            console.error('Error:', error);
            chatOutput.innerHTML += `<p><strong>Bot:</strong> Sorry, there was an error processing your request.</p>`;
        }

        chatInput.value = '';
        chatOutput.scrollTop = chatOutput.scrollHeight;
    });
});