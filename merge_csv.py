import pandas as pd

# Load SMS spam dataset (example)
sms_df = pd.read_csv("/home/shraddha/Desktop/work/Reaserch Project/sms_spam.csv")  # adjust your file name

fb_df = pd.read_csv("/home/shraddha/Desktop/work/Reaserch Project/fb_spam_extended.csv")  # your scraped posts

sms_df = sms_df[['label', 'text']]
fb_df = fb_df[['label', 'text']]

# Combine
combined_df = pd.concat([sms_df, fb_df], ignore_index=True)



# Save
combined_df.to_csv("mixed_sms_facebook_spam.csv", index=False)

print(combined_df.head())
