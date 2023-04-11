from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.contrib import messages
import pickle, soundfile, numpy as np, librosa
# Create your views here.
def sound_features(audio_file, mfcc, chroma, mel):
    with soundfile.SoundFile(audio_file) as sound_file:
        X = sound_file.read(dtype='float32')
        sample_rate = sound_file.samplerate
        if chroma:
            stft = np.abs(librosa.stft(X))
        result = np.array([])
        if mfcc:
            mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))
        if chroma:
            chroma=np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
            result=np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(X, sr= sample_rate).T, axis=0)
            result = np.hstack((result, mel))
    return result
def index(request):
    if request.method == 'POST':
        # Uploading Audio file
        uploaded_audiofile = request.FILES['audiofile']
        valid_audio_file = ['mp3', 'wav', 'm4a', 'wma']
        if uploaded_audiofile.name[-3:] not in valid_audio_file:
            print('Not an audio file')
            messages.info(request, 'Not a Valid File!! Upload Valid Files')
        else:
            messages.info(request,' Analyzing the Audio File... Wait for Few Seconds')
            file_name = default_storage.save(uploaded_audiofile.name, uploaded_audiofile)
            testingmodel = pickle.load(open('static/model.pkl', 'rb'))
            result = testingmodel.predict([sound_features(default_storage.open(file_name), mfcc=True, chroma=True, mel=True)])
            print("Emotion for Sound File: ", result)
            context = {
                'result':f'The Emotion detected in the audio file is : {result[0]}'
            }
            return render(request, 'index.html', context)
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def teams(request):
    return render(request, 'teams.html')
def dev(request):
    return render(request, 'developers.html')