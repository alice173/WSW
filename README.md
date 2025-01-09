# Walk South West

## Overview

An app to keep track of how much of the South West coastal path the user has walked.

## UX Design Process

- **User Stories:**
  - [Trello Kanban Board](https://trello.com/invite/b/6745eaca0a76ea45ef8826d6/ATTId728c7a61a787b417503eafe40cf68feC19FDF22/wsw)
- **Wireframes:**
  - [Attach or link to accessible wireframes used in the design process, ensuring high colour contrast and alt text for visual elements.]
  - [Explain the rationale behind the layout and design choices, focusing on usability and accessibility for all users, including those using assistive technologies.]
- **Design Rationale:**
  #### Colour Pallete
  The inital colour scheme from an image of the SoutWest coastal path using [coolors.co](https://coolors.co/e84610-009fe3-4a4a4f-445261-d63649-e6ecf0-000000) to generate my colour palette:

![screenshot](assets/images/palette.png)

Tints and shades generated using a [generator](https://maketintsandshades.com/)

It became apparent that an accent/complemetory colour was necessary that would stand out for some elements - I choose a yellow to reflect the gorse that grows along the path (#ffd60a)

#### Typography

Fonts are from google and hosted locally for performance gains;

- Headings/accent - [Forum](https://fonts.google.com/specimen/Forum) a classic serif font

- Base text - [Lato](https://fonts.google.com/specimen/Lato) a text that is easy to read and

I used [FontSquirrel](https://www.fontsquirrel.com/) to convert to web fonts.

## Key Features

- **Feature 1:** [Briefly describe the implemented feature.]
- **Feature 2:** [Briefly describe the implemented feature.]
- **Inclusivity Notes:**
  - [Mention how the features address the needs of diverse users, including those with SEND.]

## Deployment

- **Platform:** Heroku
- **High-Level Deployment Steps:**
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
- **Verification and Validation:**
  - Steps taken to verify the deployed version matches the development version in functionality.
  - [Include any additional checks to ensure accessibility of the deployed application.]
- **Security Measures:**
  - Use of environment variables for sensitive data.
  - Ensured DEBUG mode is disabled in production.

## AI Implementation and Orchestration

### Use Cases and Reflections:

(Highlight how prompts, such as reverse, question-and-answer or multi-step, were used to support learners with SEND or ALN where relevant.)

- **Aministration/Repetitive tasks:**
- Reflection: Strategic use of AI allowed me to perform admin tasks quicky and efficiently
- Examples: I used AI to assist with creation of user stories and then to convert them to a CSV file. AI assisted with writing a python script using Trello's Rest API that created a populated a trello card with description and checklist for each user story
- **Code Creation:**
  - Reflection: Strategic use of AI allowed for rapid prototyping, with minor adjustments for alignment with project goals.
  - Examples: Reverse prompts for alternative code solutions and question-answer prompts for resolving specific challenges.
- **Debugging:**
  - Reflection: Key interventions included resolving logic errors and enhancing maintainability, with a focus on simplifying complex logic to make it accessible.
- **Performance and UX Optimization:**
  - Reflection: Minimal manual adjustments were needed to apply AI-driven improvements, which enhanced application speed and user experience for all users.
- **Automated Unit Testing:**

  - Reflection: Adjustments were made to improve test coverage and ensure alignment with functionality. Prompts were used to generate inclusive test cases that considered edge cases for accessibility.

- **Overall Impact:**
  - AI tools streamlined repetitive tasks, enabling focus on high-level development.
  - Efficiency gains included faster debugging, comprehensive testing, and improved code quality.
  - Challenges included contextual adjustments to AI-generated outputs, which were resolved effectively, enhancing inclusivity.

## Testing Summary

- **Manual Testing:**
  - **Devices and Browsers Tested:** [List devices and browsers, ensuring testing was conducted with assistive technologies such as screen readers or keyboard-only navigation.]
  - **Features Tested:** [Summarise features tested manually, e.g., CRUD operations, navigation.]
  - **Results:** [Summarise testing results, e.g., "All critical features worked as expected, including accessibility checks."]
- **Automated Testing:**
  - Tools Used: [Mention any testing frameworks or tools, e.g., Django TestCase.]
  - Features Covered: [Briefly list features covered by automated tests.]
  - Adjustments Made: [Describe any manual corrections to AI-generated test cases, particularly for accessibility.]

## Future Enhancements

- [List potential improvements or additional features for future development.]
- Consider enhancements to improve accessibility further, such as voice input capabilities or additional language support.
