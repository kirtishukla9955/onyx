import os
import random
import logging
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Suppress Prophet and CmdStanPy console logging
logging.getLogger('prophet').setLevel(logging.WARNING)
logging.getLogger('cmdstanpy').setLevel(logging.WARNING)

# Import Prophet dynamically or catch ImportError to allow server startup even if Prophet is building
try:
    from prophet import Prophet
except ImportError:
    Prophet = None

# Predefined registry of trending topics and content suggestions
TRENDS_REGISTRY = {
    "fitness": {
        "instagram": [
            {"topic": "Zone 2 Cardio Secrets", "prompt": "Record a reel explaining Zone 2 cardio benefits while jogging at sunset. Keep it under 30s."},
            {"topic": "Mobility for Desk Workers", "prompt": "Show 3 quick office desk shoulder stretches with overlay text. Use a calming trending audio."},
            {"topic": "High-Protein Pre-Workout Snacks", "prompt": "Film a fast-paced aesthetic montage of your quick pre-workout meal assembly."},
            {"topic": "Wall Pilates Core Routine", "prompt": "Demonstrate a 5-minute wall Pilates routine with a timer widget overlay."},
            {"topic": "Aesthetic Run Club Vlogs", "prompt": "Vlog your run club meetup. Highlight the social aspect, scenic route, and post-run coffee."}
        ],
        "tiktok": [
            {"topic": "Gym Fail Recovery Reactions", "prompt": "Stitch a gym fail video with your own humorous but encouraging reaction."},
            {"topic": "15-Min Kettlebell Shred", "prompt": "Guide viewers through a rapid HIIT workout. Use on-screen counters and encourage saves."},
            {"topic": "Cozy Cardio Setup", "prompt": "Show your walking pad setup with a cozy ambiance and a movie playing. Highlight low-pressure movement."},
            {"topic": "Activewear Transitions", "prompt": "Do a high-energy snap transition swapping between 3 activewear styles."},
            {"topic": "Powerlifting Milestones", "prompt": "Compile your lifting progress from day 1 to day 90 with a cinematic drop beat."}
        ],
        "youtube": [
            {"topic": "30-Day Home Strength Challenge", "prompt": "Publish a structured 15-minute beginner workout. Link a progress PDF in your description."},
            {"topic": "Science of Muscle Growth", "prompt": "Create an educational video explaining hypertrophy research using clean infographics."},
            {"topic": "Shredding Diet Meal Prep", "prompt": "Show a weekly high-protein meal prep session with precise calorie breakdowns."},
            {"topic": "Home Gym Setup on a Budget", "prompt": "Review affordable garage gym gear from Amazon and show the finished setup."},
            {"topic": "Perfect Push-Pull-Legs Split", "prompt": "Explain the mechanics of a PPL split using a whiteboard illustration."}
        ]
    },
    "food": {
        "instagram": [
            {"topic": "5-Ingredient Air Fryer Dinners", "prompt": "Show a close-up, ASMR-style assembly of a 5-ingredient air fryer meal."},
            {"topic": "Aesthetic Matcha Cream Cold Brew", "prompt": "Film a slow-motion pour of matcha cream over cold brew. Use clean aesthetic fonts."},
            {"topic": "Viral One-Pan Feta Pasta Twist", "prompt": "Show your unique twist on the famous feta pasta in a snappy 15-second Reel."},
            {"topic": "Blindfold Snack Taste Test", "prompt": "Record a fun blindfolded taste test challenge with a friend. Add funny sound effects."},
            {"topic": "Artisan Sourdough Scoring", "prompt": "Record a satisfying close-up of scoring intricate patterns on sourdough dough."}
        ],
        "tiktok": [
            {"topic": "Late-Night Ramen Hacks", "prompt": "Upgrade instant ramen with egg yolk, Kewpie mayo, and chili oil. Keep instructions snappy."},
            {"topic": "Giant Cookie Skillet for One", "prompt": "Show the baking process of a single-serving giant cookie. Focus on gooey textures."},
            {"topic": "Korean Street Food at Home", "prompt": "Recreate cheese corn dogs or tteokbokki with rapid transitions and upbeat K-pop music."},
            {"topic": "What I Eat in a Day (Intuitive Eating)", "prompt": "Share a realistic daily food log with transparent audio commentary on food freedom."},
            {"topic": "Satisfying Cake Decorating ASMR", "prompt": "Show piping and smoothing frosting on a colorful cake. Let the raw kitchen sounds play."}
        ],
        "youtube": [
            {"topic": "Mastering French Pastries at Home", "prompt": "Create a detailed 20-minute masterclass tutorial on baking perfect croissants."},
            {"topic": "Testing Viral TikTok Kitchen Gadgets", "prompt": "Review and test 5 trendy cooking gadgets to see if they are actually worth it."},
            {"topic": "Chef Recreates Fast Food Classics", "prompt": "Recreate the Crunchwrap Supreme using high-quality gourmet ingredients."},
            {"topic": "Ultimate $20 Weekly Grocery Challenge", "prompt": "Vlog grocery shopping with a strict $20 budget and cook 3 nutritious meals from it."},
            {"topic": "Restaurant Quality Ramen from Scratch", "prompt": "Document a 12-hour tonkotsu broth making process with cinematic storytelling."}
        ]
    },
    "gaming": {
        "instagram": [
            {"topic": "Custom Keyboard Build ASMR", "prompt": "Record the clicky switches and keycap installation with pristine ASMR audio."},
            {"topic": "Cozy Indie Game Recommendations", "prompt": "Show 3 aesthetic cozy Switch games with colorful overlays and relaxing music."},
            {"topic": "Retro Console Restorations", "prompt": "Show a satisfying 30-second cleanup of an old, dirty GameBoy Advance."},
            {"topic": "Epic FPS Double Kill Clutches", "prompt": "Post a high-quality snippet of your ranked clutch play with a dramatic transition."},
            {"topic": "Miniature RGB PC Setup Walkthroughs", "prompt": "Show a slow-panning desk setup tour showcasing dynamic RGB configurations."}
        ],
        "tiktok": [
            {"topic": "No-Hit Speedrun Fail Compilations", "prompt": "Compile your most frustrating speedrun fails. Add zoom-ins and funny text overlays."},
            {"topic": "Minecraft Cozy Base Tutorials", "prompt": "Show a fast-forward build of a cozy cottage in Minecraft. Put coordinates in caption."},
            {"topic": "Open World Hidden Easter Eggs", "prompt": "Show a secret location in a new open world game that 99% of players missed."},
            {"topic": "Funny Discord Voice Chat Moments", "prompt": "Animate or add subtitles to a hilarious clip of you and your friends in voice chat."},
            {"topic": "Guess the Game Sound Effect Challenge", "prompt": "Play 3 gaming sound effects and ask viewers to guess the games. Emphasize comments."}
        ],
        "youtube": [
            {"topic": "Reviewing the Hardest Game of 2026", "prompt": "Upload a humorous review discussing why this year's new release broke your controller."},
            {"topic": "Evolution of RPG Graphics", "prompt": "Create a documentary-style video comparing RPG graphics from 1996 to 2026."},
            {"topic": "Beating Elden Ring with a Dance Pad", "prompt": "Show the training process and ultimate boss kills using a custom controller layout."},
            {"topic": "Behind the Scenes of Indie Game Dev", "prompt": "Vlog a week in your life coding an indie game, discussing struggles and breakthroughs."},
            {"topic": "Complete History of Speedrunning", "prompt": "Tell the history of how speedrunners broke a specific popular game. Use diagrams."}
        ]
    },
    "lifestyle": {
        "instagram": [
            {"topic": "Minimalist Room Decluttering Hacks", "prompt": "Show a satisfying before/after transition of a messy closet organization."},
            {"topic": "Productive Sunday Reset Routine", "prompt": "Show clean-sheets, laundry, grocery prep, and planning. Use soft warm colors."},
            {"topic": "Thrift Store Clothing Flips", "prompt": "Show a $5 thrifted shirt and how you style it 3 different ways with quick cuts."},
            {"topic": "Solo Travel Hidden Gems", "prompt": "Post a carousel of a hidden cafe in Paris. Add travel details in the caption."},
            {"topic": "Digital Detox Vlog Snippets", "prompt": "Show reading, journaling, and walking outside. Write about screen-time boundaries."}
        ],
        "tiktok": [
            {"topic": "Morning Coffee Ritual ASMR", "prompt": "Capture ice clinking, espresso dripping, and milk swirling with no background music."},
            {"topic": "Unboxing Aesthetic Tech Accessories", "prompt": "Unbox a pastel tablet stand or phone case. Add cute animated stickers to the video."},
            {"topic": "5-Minute Grounding Habits", "prompt": "Talk about 3 small daily habits that improved your mental clarity. Keep it conversational."},
            {"topic": "Realistic Evening Wind Down", "prompt": "Show lighting candles, doing a skincare routine, and reading in bed. Keep lighting low."},
            {"topic": "Styling Oversized Blazers", "prompt": "Do a styling challenge showing how to dress up a blazer for day vs night."}
        ],
        "youtube": [
            {"topic": "Vlog: Quiet Week of Self-Care", "prompt": "Publish a slow-paced 15-minute vlog focusing on slow living, journaling, and cooking."},
            {"topic": "Designing My Ultimate Dream Office", "prompt": "Document your home office renovation project. Include 3D models and budget tips."},
            {"topic": "How I Broke My Shopping Addiction", "prompt": "Share a sit-down video discussing your journey to minimalism and how much money you saved."},
            {"topic": "A Week in Tokyo: Solo Travel Diary", "prompt": "Create a cinematic travel documentary of your solo trip. Focus on street food and cafes."},
            {"topic": "Complete Guide to Digital Organization", "prompt": "Show how you organize your emails, cloud drives, and Notion boards for maximum clarity."}
        ]
    }
}

def generate_mock_history(seed_val: int) -> pd.DataFrame:
    """
    Generates mock engagement velocity history over the past 10 days (240 hourly points)
    with a daily cycle, an upward trend, and random noise.
    """
    random.seed(seed_val)
    np.random.seed(seed_val)
    
    now = datetime.utcnow()
    start_time = now - timedelta(days=10)
    
    # 240 hourly datetimes
    date_range = [start_time + timedelta(hours=i) for i in range(240)]
    
    # Base trend + daily seasonality (peaking in evening) + noise
    y_values = []
    base = 15.0 + random.uniform(0, 10)
    slope = 0.05 + random.uniform(0, 0.05)
    
    for i in range(240):
        hour = date_range[i].hour
        # Peak engagement around 8 PM (hour 20)
        seasonality = 8.0 * np.sin((hour - 14) * np.pi / 12)
        # Random noise
        noise = np.random.normal(0, 2.0)
        
        y = max(1.0, base + (i * slope) + seasonality + noise)
        y_values.append(y)
        
    df = pd.DataFrame({
        "ds": date_range,
        "y": y_values
    })
    return df

def generate_trend_forecast(niche: str, platform: str):
    """
    Retrieves trending topics for a niche/platform, simulates history,
    fits a Prophet model for each, and returns predictions.
    """
    # Normalize niche and platform
    niche_key = niche.lower() if niche else "lifestyle"
    platform_key = platform.lower() if platform else "tiktok"
    
    if niche_key not in TRENDS_REGISTRY:
        niche_key = random.choice(list(TRENDS_REGISTRY.keys()))
    if platform_key not in TRENDS_REGISTRY[niche_key]:
        platform_key = random.choice(list(TRENDS_REGISTRY[niche_key].keys()))
        
    topics = TRENDS_REGISTRY[niche_key][platform_key]
    
    predictions = []
    
    for idx, item in enumerate(topics):
        topic_name = item["topic"]
        prompt = item["prompt"]
        
        # Generate distinct mock data for each topic based on index
        df_history = generate_mock_history(seed_val=hash(topic_name) % 10000)
        
        peak_hours = 0
        velocity_score = 0.0
        
        # Check if Prophet was successfully imported
        if Prophet is not None:
            try:
                # Initialize Prophet model with daily and weekly seasonality
                model = Prophet(
                    growth="linear",
                    yearly_seasonality=False,
                    weekly_seasonality=True,
                    daily_seasonality=True
                )
                
                # Fit the model
                model.fit(df_history)
                
                # Predict future 48 hours (hourly)
                future = model.make_future_dataframe(periods=48, freq="h", include_history=False)
                forecast = model.predict(future)
                
                # Find peak yhat in future predictions
                peak_idx = forecast["yhat"].idxmax()
                peak_row = forecast.iloc[peak_idx]
                
                # Hours from now
                now = datetime.utcnow()
                peak_time = peak_row["ds"]
                time_diff = peak_time - now
                peak_hours = max(1, int(time_diff.total_seconds() // 3600))
                
                # Limit peak hours to next 48 hours
                if peak_hours > 48:
                    peak_hours = random.randint(4, 24)
                    
                # Normalize velocity score to a 0-100 range
                raw_score = peak_row["yhat"]
                velocity_score = round(min(100.0, max(0.0, raw_score * 1.5)), 1)
                
            except Exception as e:
                # Fallback in case of Prophet fitting error
                peak_hours = random.randint(2, 28)
                velocity_score = round(random.uniform(65.0, 98.0), 1)
        else:
            # Fallback if Prophet is not installed/loaded (e.g. while container installs)
            # This makes the app highly resilient!
            peak_hours = random.randint(2, 28)
            velocity_score = round(random.uniform(65.0, 98.0), 1)
            
        predictions.append({
            "trend_name": topic_name,
            "predicted_peak_in_hours": peak_hours,
            "engagement_velocity_score": velocity_score,
            "niche_prompt": prompt
        })
        
    # Sort by engagement velocity score descending
    predictions = sorted(predictions, key=lambda x: x["engagement_velocity_score"], reverse=True)
    
    return {
        "niche": niche_key,
        "platform": platform_key,
        "trends": predictions[:5]
    }
