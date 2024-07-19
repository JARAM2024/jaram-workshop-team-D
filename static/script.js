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