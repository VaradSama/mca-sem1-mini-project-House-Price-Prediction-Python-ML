from django.shortcuts import render, redirect, get_object_or_404
from .forms import HouseForm
from .models import Prediction
from django.conf import settings
import os, joblib, numpy as np
MODEL_PATH = os.path.join(settings.ML_MODELS_DIR, 'house_model_v1.joblib')

def home_view(request):
    return render(request, "base.html")

def load_model():
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            return None
    return None

def featurize(cleaned):
    loc = 1 if cleaned['location'].lower() == 'urban' else 0
    garage = 1 if cleaned['has_garage'] == 'yes' else 0
    return [cleaned['total_sqft'], cleaned['bhk'], cleaned['bath'], cleaned['year_built'], loc, garage]


def predict_view(request):
    form = HouseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        X = np.array(featurize(data)).reshape(1, -1)
        model = load_model()
        predicted = None
        if model is not None:
            predicted = float(model.predict(X)[0])
        
        # Save prediction with user
        pred = Prediction.objects.create(
            user=request.user,            # <-- link to logged-in user
            input_features=data,
            predicted_price=predicted or 0.0
        )
        return redirect('result', pk=pred.id)
    
    return render(request, 'homes/predict.html', {'form': form})

def result_view(request, pk):
    pred = get_object_or_404(Prediction, pk=pk)
    return render(request, 'homes/result.html', {'pred': pred})
