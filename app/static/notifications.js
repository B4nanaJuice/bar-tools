function createNotification(type, title, description) {

    let notification = document.createElement('div');
    notification.classList.add('notification');
    notification.classList.add(`notification-${type}`);

    notification.innerHTML = `
        <button class="icon-only" onclick="this.parentElement.remove();">
            <svg width="20" height="20" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M25 1L1 25M1 1L25 25" stroke="#1B1107" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </button>
    `;

    let notificationTitle = document.createElement('h2');
    notificationTitle.classList.add('notification-title');
    notificationTitle.innerText = title;

    let notificationDesc = document.createElement('p');
    notificationDesc.classList.add('notification-description');
    notificationDesc.innerHTML = description;

    notification.appendChild(notificationTitle);
    notification.appendChild(notificationDesc);

    notification.innerHTML += "<div class=\"progress-bar\" style=\"height: 4px; margin-top: 12px;\"><div class=\"bar\" style=\"height: 4px;\"></div></div>";

    document.querySelector('.notifications').appendChild(notification);

    setTimeout(() => {
        notification.querySelector('.progress-bar .bar').style.width = '100%';

        setTimeout(() => {
            notification.remove();
        }, 2000);
    }, 100);
}