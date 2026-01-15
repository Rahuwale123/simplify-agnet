# Frontend Documentation: Job Creation Flow

## Overview
The frontend interacts with the Simplifi Agent backend to guide the user through a job creation workflow. The "Create Job" button logic is a key part of this interaction.

## How the "Create Vacancy Now" Button Appears

1.  **Backend Signal**:
    -   When the users completes the data collection phase, the backend agent (in `app/agents/base_agent.py`) executes the `submit_job` tool.
    -   The agent returns a special JSON payload in its final answer:
        ```json
        {
          "ui_action": "show_completion_buttons",
          "create_job_now": true,
          "draft_data": { ...collected fields... }
        }
        ```

2.  **Frontend Detection** (`frontend/script.js`):
    -   The `formatContent(content)` function scans all incoming AI messages.
    -   It looks for the specific marker string: `"ui_action": "show_completion_buttons"`.
    -   If found, it parses the JSON block.

3.  **Rendering**:
    -   The `renderSummary(data)` function is called with the drafted job data.
    -   This function returns the HTML for the "Job Summary Card", which includes the button:
        ```html
        <button class="create-job-btn" onclick='createJob()'>
            <i class="fas fa-rocket"></i> Create Vacancy Now
        </button>
        ```

## What Happens When Clicked

When the user clicks "Create Vacancy Now", the following sequence is triggered:

1.  **Function Call**: The global `window.createJob()` function in `script.js` is executed.

2.  **UI Feedback**:
    -   The button text changes to `<i class="fas fa-spinner fa-spin"></i> Creating...`.
    -   The button is disabled to prevent double-submissions.

3.  **API Request**:
    -   A `POST` request is sent to `http://13.60.157.40:8000/api/v1/jobs/create`.
    -   **Headers**: 
        -   `token`: The Bearer token from the configuration settings (JWT).
        -   `programId`: The selected Program UUID.
    -   **Body**:
        -   `userId`: The current session/user ID.

4.  **Response Handling**:
    -   **Success (200 OK)**:
        -   The VMS returns the created job details.
        -   A success message is appended to the chat: `🎉 **Success!** Your job vacancy has been created successfully!`.
        -   The button updates closer to "Job Created".
    -   **Error**:
        -   If the VMS or Backend returns an error (e.g., 403 Forbidden, 400 Bad Request), an error message is displayed in the chat.
        -   The button resets to allow retrying.

## Key Files
-   **`frontend/script.js`**: Contains the logic for `formatContent` (detection) and `createJob` (execution).
-   **`frontend/style.css`**: Defines the styles for `.job-summary-card` and `.create-job-btn`.
