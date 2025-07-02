# Sage Endocrine

A modern Django-based endocrine care management system for handling patient prescriptions and doctor/admin remarks, with a focus on clear workflow, robust status tracking, and a user-friendly interface for endocrinology clinics.

## Features
- **Two user types:** Patients and Admin/Doctors
- **Patient:**
  - Register, login, and upload prescription files (stored in the database)
  - Track prescription status (pending/done)
  - View doctor remarks (only the latest, never history)
- **Admin/Doctor:**
  - Login via a separate admin portal
  - View all patient prescriptions
  - Add, edit, and update remarks for each prescription
  - Revert prescription status to pending (for further review or correction)
  - Edit remarks after reverting
  - Dashboard with clear status, timestamps, and action buttons
- **Modern UI:**
  - Bootstrap 5 styling
  - Color-coded rows for status (blue for reviewed, yellow for reverted, etc.)
  - Tooltips and modals for long remarks

## Project Structure
- `core/` — Main Django app (models, views, templates)
- `templates/core/` — All HTML templates (Bootstrap 5)
- `media/` — (Unused, as files are stored in DB)
- `db.sqlite3` — SQLite database (default for easy setup)

## Database Logic
- **Prescription**: Each prescription is linked to a patient, stores the file as binary, and tracks status (`pending` or `done`).
- **DoctorRemark**: One-to-one with Prescription. Only one remark per prescription. Editing a remark updates the same record.
- **Status Flow:**
  - `pending` (awaiting review)
  - `done` (remark added)
  - Admin can revert to `pending` (for correction), but the remark is retained and can be edited.

## User Flows
### Patient
1. Register and login
2. Upload prescription (file stored in DB)
3. See all uploaded prescriptions and their status
4. When a doctor adds a remark, see a "View Remark" badge (with modal for long remarks)
5. Only the latest remark is ever visible

### Admin/Doctor
1. Login via `/admin-login/`
2. See all prescriptions in a dashboard
3. For each prescription:
   - If no remark: **Add Remark**
   - If reviewed: **Edit Remark** and **Revert to Pending** (row is blue)
   - If reverted: **Edit Remark** only (row is yellow)
4. Can edit remarks after reverting, and status changes accordingly
5. All actions are color-coded and have tooltips for clarity

## Setup Instructions
1. **Clone the repo:**
   ```bash
   git clone https://github.com/Priyamkeshwa/HMS_v2.git
   cd HMS_v2
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install django
   ```
4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```
6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
7. **Access the app:**
   - Patient: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Admin/Doctor: [http://127.0.0.1:8000/admin-login/](http://127.0.0.1:8000/admin-login/)

## Troubleshooting
- **Database errors (e.g., missing columns):**
  - Delete `db.sqlite3` and all migration files in `core/migrations/` except `__init__.py`, then re-run migrations.
- **No admin user:**
  - Use `createsuperuser` as above.
- **Static files not loading:**
  - Ensure you have an internet connection for Bootstrap CDN, or set up static files locally.
- **File uploads:**
  - Files are stored in the database, not the filesystem.

## Customization
- To use a different database, update `hospitalmgmt/settings.py` and install the appropriate driver.
- To add more user types or features, extend the models and views in `core/`.

## Contributing
Pull requests and suggestions are welcome!

## License
MIT License

## Accessing the Database & Running SQL Queries

You can inspect or run raw SQL queries on the SQLite database in two ways:

### 1. Using the Django Shell
- Start the shell:
  ```bash
  python manage.py dbshell
  ```
  or (for advanced queries and ORM):
  ```bash
  python manage.py shell
  ```
- In the shell, you can run raw SQL (with `dbshell`) or use Django ORM (with `shell`).

### 2. Using the SQLite3 CLI
- Open the database directly:
  ```bash
  sqlite3 db.sqlite3
  ```
- Example SQL commands:
  - List tables:
    ```sql
    .tables
    ```
  - Show schema for a table:
    ```sql
    .schema core_prescription
    ```
  - Run a query:
    ```sql
    SELECT * FROM core_prescription;
    ```
- To exit:
  ```sql
  .exit
  ```

**Note:** Always back up your database before running destructive queries.

## Branding
- **Header:** Simple, soft blue with DNA icon and app name 'Sage Endocrine'.
- **Footer:** Simple, soft blue with copyright and 'Sage Endocrine'.

## Instruction Manual: Workflows & UI Actions

### Patient Workflows

#### 1. Registration & Login
- Go to the patient registration page and fill in your details.
- After registering, log in using your credentials.

#### 2. Uploading a Prescription
- On your dashboard, click the "Upload Prescription" button.
- Select your prescription file (PDF, image, etc.) and submit.
- The prescription will appear in your dashboard with status "Pending".

#### 3. Tracking Prescription Status
- Each prescription row shows its current status:
  - **Pending:** Awaiting doctor review.
  - **Done:** Doctor has reviewed and added a remark.
- A progress bar visually indicates the review stage.

#### 4. Viewing Doctor Remarks
- If a remark is available, a green badge appears.
- For long remarks, click "View Full Remark" to open a modal with the complete text.
- Only the latest remark is ever shown.

#### 5. Viewing Prescriptions
- Click the "View" button to open your prescription in a new browser tab (PDF/image).

---

### Doctor/Admin Workflows

#### 1. Login
- Use the admin login page to access the doctor dashboard.

#### 2. Reviewing Prescriptions
- The dashboard lists all patient prescriptions with avatars and status highlights.
- Quick stats at the top show counts of pending and reviewed prescriptions.
- Each row is color-coded:
  - **Blue:** Reviewed (done) with a remark.
  - **Yellow:** Pending but has a remark (after revert).
  - **No color:** Pending, no remark.

#### 3. Adding a Remark
- For pending prescriptions, click "Add Remark".
- Enter your feedback and submit. The status changes to "Done".

#### 4. Editing a Remark
- For reviewed prescriptions, click "Edit Remark" (yellow button).
- Update your feedback and save.

#### 5. Reverting to Pending
- If you want to change your feedback, click "Revert to Pending" (red outline button).
- The row turns yellow, and only "Edit Remark" is available.
- You can now update the remark and save.
- Once saved, the status returns to "Done" (blue row).

#### 6. Viewing Uploaded Prescriptions
- Click the "View" link to open the prescription file in a new tab.

---

### UI/UX CTAs & Visual Cues
- **Buttons:**
  - Blue: Add Remark
  - Yellow: Edit Remark
  - Red outline: Revert to Pending
  - Green: View (prescription)
- **Badges:**
  - Status and remarks are shown as colored badges for clarity.
- **Progress Bars:**
  - Indicate review progress for patients.
- **Avatars:**
  - Patient avatars for a personal touch.
- **Sidebar (Doctor):**
  - Quick navigation (future expansion).

---

### Troubleshooting & Tips
- If you encounter errors, check the status bar or alert messages for feedback.
- For database issues, see the "Accessing the Database" section above.
- Only the latest remark is visible to patients; history is not shown.
- All files are stored securely in the database and served inline for easy viewing.

---

For more details, see the screenshots and UI/UX philosophy sections above. 