**Events for Amplitude**

Minimal set of events in Amplitude would cover the described user flow:



**app\_install**: Track the initial installation of the application. **Properties**: event\_id, device\_id, device\_type, session\_id, user\_id, timestamp, platform, region, language, app\_version.



**app\_opened**: Triggers when the user launches the application. **Properties**: event\_id, device\_id, device\_type, session\_id, user\_id, timestamp, platform, region, language, app\_version.



**home\_screen\_viewed**: Log when the user views the main home screen. **Properties**: event\_id, device\_id, device\_type, session\_id, user\_id, timestamp, platform, region, language, app\_version, screen, has\_prior\_history (boolean), subscription\_type.



**input\_field\_tapped**: Record when the user taps on the input field. **Properties**: event\_id, device\_id, device\_type, session\_id, user\_id, timestamp, platform, region, language, app\_version, screen, subscription\_type, input\_method (keyboard, voice, add file).



**premium\_features\_tapped**: Record when the user taps on the 'Premium Features' view. **Properties**: event\_id, device\_id, device\_type, session\_id, user\_id, timestamp, platform, region, language, app\_version, screen, subscription\_type, premium\_feature\_id.



**get\_help\_tapped**: Record when the user taps on the 'Get Help with Any Task' view. **Properties**: event\_id, device\_id, device\_type, session\_id, user\_id, timestamp, platform, region, language, app\_version, screen, subscription\_type, get\_help\_task\_id.



**themed\_tapped**: Record when the user taps on the 'Themed' view. **Properties**: event\_id, device\_id, device\_type, session\_id, user\_id, timestamp, platform, region, language, app\_version, screen, subscription\_type, theme\_view\_id.



**model\_choose\_tapped**: Record when the user taps on the model type field. Properties: event\_id, device\_id, device\_type, session\_id, user\_id, timestamp, platform, region, language, app\_version, screen, subscription\_type, initial\_ai\_model\_type.



**back\_button\_tapped**: Record when the user taps on the back button. Properties: event\_id, device\_id, device\_type, session\_id, user\_id, timestamp, platform, region, language, app\_version, screen, subscription\_type, ai\_model\_type.



**question\_sent**: Record when the user sends their question to the AI chat. **Properties**: event\_id, device\_id, device\_type, session\_id, user\_id, timestamp, platform, region, language, app\_version, screen, message\_length, task\_type (work, social media, gaming, health, summarizing, email, generate picture), is\_free\_mode (boolean), subscription\_type, is\_file\_attached, file\_type, file\_size, ai\_model\_type.



**answer\_received**: Log when the AI's response is displayed to the user. **Properties**: event\_id, device\_id, device\_type, session\_id, user\_id, timestamp, platform, region, language, app\_version, screen, response\_length, response\_time\_ms, success\_status (success, error, timeout), subscription\_type.



**error\_displayed**: If the user receives an error message instead of a response, log this event. **Properties**: event\_id, device\_id, device\_type, session\_id, user\_id, timestamp, platform, region, language, app\_version, screen, error\_type (network\_error, processing\_error), error\_message, subscription\_type.



**answer\_action\_tapped** (optional): If the user copies, shares, or provides feedback on the answer. **Properties**: event\_id, device\_id, device\_type, session\_id, user\_id, timestamp, platform, region, language, app\_version, screen, response\_action\_type (copy, share, like, compare models), subscription\_type.



**Metrics for the Flow**

Key metrics to calculate within this flow are:



**Conversion Rate**: The percentage of users who visit the home screen (or open the app) and successfully received at least one answer.



**Flow Conversion Rate** (funnel): The percentage of users who start the flow (home screen view) and drop off at each step of the flow (home screen -> tap input -> send question -> receive answer) to identify bottlenecks and finally successfully receive an answer.



**Engagement Rate**: The percentage of users who send at least one question to the all number of daily active users.



**Average Messages Per Session** (or Day): The average number of question\_sent events within a single user session (or Day).



**Daily active users (DAU)**: the number of users who trigger a specific event in a day.



**Time to Answer**: The average time (in milliseconds or seconds) from question\_sent to answer\_received.



**Error Rate**: The percentage of question\_sent events that result in an error\_displayed event.



**Time to Message Sent:** The average time (in seconds) from the input\_field\_tapped to question\_sent.



**Average Message Length**: The mean character count of the message\_length property to understand user query complexity.





**Hypothesis \& Experiment Design**





**Hypothesis**: Changing the placeholder text in the input field from 'Type your message...' to 'Tell me what to write...' will increase the number of questions submitted by first-time users.

**Experiment Design** (A/B Test)

**Target Audience**: First-time users who have installed the app and reached the chat screen but have not yet submitted a question.

**Groups**:

Control Group (Group A - 50% of users): Sees the current, generic placeholder text: "Type your message...".

Test Group (Group B - 50% of users): Sees the new, action-oriented placeholder text: "Tell me what to write...".

**Randomization**: Users are randomly assigned to either Group A or Group B upon their first app launch.

**Key Metrics**: The percentage of users in each group who successfully trigger the question\_sent event (Conversion Rate).

**Duration**: Run the experiment until statistical significance is achieved. It is better to collection data across different days and times.

**Analysis**: Compare the conversion rates of the two groups. If Group B has a statistically significant higher conversion rate, the hypothesis is confirmed, and the new design is successful.





**Hypothesis**: Replacing the empty chat screen with a display of several clickable suggested prompts ('Write a social media post', 'Paraphrase a paragraph', 'Explain a term') will increase the conversion rate for sending the first message, as it reduces 'blank page syndrome' and immediately showcases the app's capabilities.

**Experiment Design** (A/B Test)

**Target Audience**: First-time users who have reached the chat screen but have not yet submitted a question.

**Groups**:

Control Group (Group A - 50% of users): Sees the current empty chat screen or simple input field placeholder ("Type your message...").

Test Group (Group B - 50% of users): Sees a redesigned chat screen featuring 3-4 visible, clickable buttons/cards, each with a prompt idea ('Write a social media post', 'Paraphrase a paragraph', 'Explain a term'). Tapping a card pre-fills the input field with the text and moves the cursor to the end of the message.

**Randomization**: Users are randomly assigned to either Group A or Group B upon their first app launch.

**Key Metrics**: The percentage of users in each group who successfully trigger the question\_sent event (Conversion Rate). Secondary metrics include average messages per session and time to first message.

**Duration**: Run the experiment until statistical significance is achieved. It is better to collection data across different days and times.

**Analysis**: Compare the conversion rates of the two groups. If Group B has a statistically significant higher conversion rate, the hypothesis is confirmed, and the new design is successful.





**Hypothesis**: Adding a small block of social proof to the home screen (examples: 'Over 1 million people already use ChatOn for work and creativity', 'Trusted by 1 Million+ Users') will boost user trust in the product and increase subscribers (and overall user engagement).

**Experiment Design** (A/B Test)

**Target Audience**: Users who have opened the app at least once but haven't used a premium feature or subscribed (focusing on building trust).

**Groups**:

Control Group (Group A - 50% of users): Sees the standard home screen interface without any explicit social proof text.

Test Group (Group B - 50% of users): Sees a small banner or text element (e.g., at the bottom of the screen or near the input field) displaying the social proof message: 'Trusted by 1 Million+ Users'.

**Randomization**: Users are randomly assigned to either Group A or Group B upon their first app launch.

**Key Metrics**: The primary metric is 'Average Messages Per Session' (overall user engagement). Secondary metrics include session duration, and the Conversion Rate to the premium subscription.

**Duration**: Run the experiment until statistical significance is achieved. It is better to collection data across different days and times.

**Analysis**: Analyze 'Average Messages Per Session' over the testing period for both groups. A significant increase in this metric for Group B would validate the hypothesis and leading to more usage.





**Hypothesis**: Adding a banner on the home screen that allows users to select different AI models with brief feature descriptions will increase user satisfaction, as users feel more control over the application's output and discover advanced functionalities sooner.

**Experiment Design** (A/B Test)

**Target Audience**: Users who have opened the app at least once and have a trial subscription.

**Groups**:

Control Group (Group A - 50% of users): The current home screen layout is maintained, without the AI model selection banner.

Test Group (Group B - 50% of users): A new, tappable AI model selection banner is added below the "Premium Features" section. Tapping this banner opens chat screen as usual.

**Randomization**: Users are randomly assigned to either Group A or Group B upon their first app launch.

**Key Metrics**: The percentage of users in each group who successfully trigger the question\_sent event (Conversion Rate).

**Duration**: Run the experiment until statistical significance is achieved. It is better to collection data across different days and times.

**Analysis**: Compare the conversion rates of the two groups. If Group B has a statistically significant higher conversion rate, the hypothesis is confirmed, and the new design is successful.



