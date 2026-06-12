# Custom HRMS PWA - SLHRM

Custom mobile app for HRMS with check-in logs, leave management, and salary viewing.

## Features

- **Home Dashboard**: Check-in status, quick actions
- **Check-in Logs**: Supervisors can view team check-in/out logs
- **Leaves**: Apply for and view leave applications
- **Claims**: Submit and track expense claims
- **Salary**: View salary slips
- **Profile**: Employee profile information

## Installation

1. Get the app:
```bash
bench get-app https://github.com/kumuduraj/custom_hrms_pwa.git
bench --site YOUR-SITE install-app custom_hrms_pwa
```

2. Build assets:
```bash
bench build --app custom_hrms_pwa
```

3. Deploy to Docker:
```bash
docker cp custom_hrms_pwa frappe_docker-backend-1:/home/frappe/frappe-bench/apps/
docker cp custom_hrms_pwa frappe_docker-frontend-1:/home/frappe/frappe-bench/apps/
docker exec frappe_docker-backend-1 bench build --app custom_hrms_pwa
```

4. Access PWA:
```
https://YOUR-SITE/hrms/home
```

## Configuration

- **Logo**: Upload company logo in Company DocType
- **Theme**: Edit `hooks.py` to change colors
- **Navigation**: Edit `frontend/src_override/components/BottomNav.vue`

## Tech Stack

- Vue.js 3
- Frappe UI
- Pinia (State Management)
- Vue Router
- PWA (Progressive Web App)
