import os
import json
import librosa

DATA_PATH = null
JSON_PATH = null
SAMPLE_RATE = 22050 # 1 sec worth of sound ( in terms of librosa ) (this is the sample rate)

# n_mfcc is the num of mfcc, hop length is division of time segements, fft is window through a FFT
def preprocess(data_path, json_path, num_mfcc=13, jump=512, num_fft=2048):
    # data dictionary
    data = {
        "mapped": [],
        "which": [],
        "MFCC": [],
        "file": []
    }

    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):

        # We need to ensure that we're not at a root level

        if dirpath is not data_path:
            # update mappings 

            category = dirpath.split("/") # dataset/down => [dataset, down]
            data["mapped"].append(category)
            
            # loop through all the filenames and extract MFCCs
            for f in filenames:

                # get file path
                file_path = os.path.join(dirpath, f)

                # load audio file
                signal, sr = librosa.load(file_path)

                # ensure the audio file is at least 1 sec
                if len(signal) >= SAMPLE_RATE:
                    
                    # Make signal 1 second
                    signal = signal[:SAMPLE_RATE]

                    # extract MFCCs
                    MFCCs = librosa.feature.mfcc(signal, num_mfcc, jump, num_fft)

                    # store data
                    data["which"].append(i-1)
                    data["MFCCs"].append(MFCCs.T.tolist())
                    data["file"].append(file_path)
                    print(f"{file_path}: {i-1}")

    # store in json file
    # Added additional comment to help teach git
    with open(json_path, "w") as fp:
        json.dump(data, fp, indent=4)

if __name__ == "__main__":
    preprocess(DATA_PATH, JSON_PATH)