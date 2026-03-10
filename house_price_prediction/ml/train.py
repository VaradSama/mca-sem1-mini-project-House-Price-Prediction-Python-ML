import numpy as np, pandas as pd, joblib, os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Output folder
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'ml_models')
os.makedirs(OUT_DIR, exist_ok=True)
MODEL_PATH = os.path.join(OUT_DIR, 'house_model_v1.joblib')

# Generate synthetic house dataset
rng = np.random.RandomState(42)
N = 2000

total_sqft = rng.uniform(300, 5000, N)
bhk = rng.choice([1, 2, 3, 4, 5], N, p=[0.1, 0.25, 0.4, 0.2, 0.05])
bath = (bhk + rng.poisson(1, N)).clip(1, 6)
year_built = rng.choice(range(1950, 2022), N)
loc = rng.choice([0, 1], N, p=[0.4, 0.6])   # 1 = Urban, 0 = Rural
garage = rng.choice([0, 1], N, p=[0.7, 0.3])

# Price formula with stronger differences
base_price = total_sqft * (3000 + 800 * bhk)    # Higher sqft + bhk influence
age_factor = (2022 - year_built) * 1000         # Older houses lose value
loc_multiplier = np.where(loc == 1, 1.3, 0.8)   # Urban more expensive, Rural cheaper
garage_factor = garage * 50000                  # Garage adds value

price = (base_price * loc_multiplier) - age_factor + garage_factor + rng.normal(0, 50000, N)

# Prepare dataset
X = pd.DataFrame({
    'total_sqft': total_sqft,
    'bhk': bhk,
    'bath': bath,
    'year_built': year_built,
    'loc': loc,
    'garage': garage
})
y = price

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline with scaling + RandomForest
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('reg', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train
pipeline.fit(X_train, y_train)
print('Model trained. Test R2:', pipeline.score(X_test, y_test))

# Save model
joblib.dump(pipeline, MODEL_PATH)
print('Saved model to', MODEL_PATH)
