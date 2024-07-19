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
