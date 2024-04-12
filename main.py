import numpy as np
import sounddevice as sd
import wavio as wv
from os import path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import sys
import librosa
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

FORM_CLASS, _ = loadUiType(
    path.join(path.dirname(__file__), "security_voice_code_access.ui"))


class VoiceCodeAnalyzer:
    def __init__(self):
        self.passcode_sentences = ["Open middle door",
                                   "Unlock the gate", "Grant me access"]

    def euclidean_distance_measure(self, database_list, record_list):
        distance_list = []
        for data in database_list:
            distance, _ = fastdtw(data, record_list, dist=euclidean)
            distance_list.append(round(distance, 2))
        return distance_list

    def compute_mfcc(self, file_path):
        audio_data, sampling_rate = librosa.load(file_path)
        mfcc = librosa.feature.mfcc(y=audio_data, sr=sampling_rate, n_mfcc=100)
        return mfcc.T


class UISettings:
    def __init__(self, access_label, access_icon):
        self.selected_mode = None
        self.selected_users = []  # For Security voice fingerprint mode
        self.access_label = access_label
        self.access_icon = access_icon

    def toggle_recording(self, bg_color, mic_button):
        existing_stylesheet = mic_button.styleSheet()
        new_styles = f"QPushButton {{background-color: {bg_color};}}"
        updated_stylesheet = existing_stylesheet + new_styles
        mic_button.setStyleSheet(updated_stylesheet)

    def modify_table(self, similarity, similarity_table):
        for index, value in enumerate(similarity):
            str_value = str(value)
            # Create a QTableWidgetItem with the string value
            item = QTableWidgetItem(str_value)
            similarity_table.setItem(index-1, 1, item)

    def change_access(self, label_text, label_color, access_icon):
        self.access_label.setText(f"{label_text}")
        self.access_label.setStyleSheet(f"color: {label_color};")
        self.access_icon.setPixmap(access_icon.scaled(
            access_icon.size(), Qt.KeepAspectRatio))


class DataBase():
    def __init__(self, file_path):
        self.mfcc_list = []
        self.file_path = file_path
        self.analyzer = VoiceCodeAnalyzer()
        self.get_mfcc()

    def get_mfcc(self):
        self.mfcc_list = self.analyzer.compute_mfcc(
            self.file_path)


class Record(FigureCanvas):
    def __init__(self, parent=None, spectrogram_data=[]):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.mfcc_list = []

        self.analyzer = VoiceCodeAnalyzer()
        super().__init__(self.fig)

    def record_audio(self, duration=2, filename="recordings/recorded_audio.wav"):
        fs = 44100
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()
        wv.write(filename, recording, fs, sampwidth=2)
        self.show_spectrogram()
        self.mfcc_list = self.analyzer.compute_mfcc(
            filename)

    def show_spectrogram(self):
        audio_data, sampling_rate = librosa.load(
            "recordings/recorded_audio.wav")
        self.ax.clear()  # Clear previous content from the axes
        self.ax.specgram(audio_data, Fs=sampling_rate, cmap='viridis')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Frequency (Hz)')
        self.draw()


class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.database_dictionary = {
            "OpenTheDoor": {'mariamH': [], 'mariamM': [], 'ali': [], 'mina': [], 'ahmed': [], 'hazem': [], 'nourhan': [], 'mayar': []},
            "UnlockMiddleGate": {'mariamH': [], 'mariamM': [], 'ali': [], 'mina': [], 'ahmed': [], 'hazem': [], 'nourhan': [], 'mayar': []},
            "GiveMeAccess": {'mariamH': [], 'mariamM': [], 'ali': [], 'mina': [], 'ahmed': [], 'hazem': [], 'nourhan': [], 'mayar': []}
        }
        self.similarity = []
        self.sentences = ["OpenTheDoor", "UnlockMiddleGate", "GiveMeAccess"]
        self.people = ["mariamH", "mariamM", "ali",
                       'mina', 'ahmed', 'hazem', 'nourhan', 'mayar']

        self.spectrogram = Record()
        self.spectogram_layout = QHBoxLayout(self.spectrogram_widget)
        self.spectogram_layout.addWidget(self.spectrogram)
        self.create_database_objects()
        self.mic_button.clicked.connect(self.toggle_recording)
        self.uisettings = UISettings(self.access_label, self.access_icon)
        self.locked = QPixmap("icons/locked.png")
        self.unlocked = QPixmap("icons/unlocked.png")
        self.sentence_threshold = 10000
        self.person_threshold = 8500

    def create_database_objects(self):
        for sentence in self.sentences:
            for person in self.people:
                path = f"dataset/{sentence}/{person}/sample{1}.wav"
                database_obj = DataBase(path)
                self.database_dictionary[sentence][person] = database_obj

    def toggle_recording(self):
        self.uisettings.toggle_recording('darkred', self.mic_button)
        self.spectrogram.record_audio()
        self.uisettings.toggle_recording('white', self.mic_button)

        sentence_similarity_score, sentence_max_similarity_index, sentence_detected = self.calc_similarity(
            self.sentences, False)
        person_similarity_score, person_max_similarity_index, person_detected = self.calc_similarity(
            self.people, True, sentence_detected)

        if self.mode_1_radiobtn.isChecked():
            if sentence_similarity_score[sentence_max_similarity_index] < self.sentence_threshold:
                self.uisettings.change_access(
                    'Granted', 'green', self.unlocked)
            else:
                self.uisettings.change_access('Denied', 'red', self.locked)

        elif self.mode_2_radiobtn.isChecked():
            if sentence_similarity_score[sentence_max_similarity_index] < self.sentence_threshold and person_similarity_score[person_max_similarity_index] < self.person_threshold:
                self.uisettings.change_access(
                    f"Hello {person_detected}", 'green', self.unlocked)
            else:
                self.uisettings.change_access('Denied', 'red', self.locked)

        self.similarity = sentence_similarity_score + person_similarity_score
        self.uisettings.modify_table(self.similarity, self.similarity_table)

    def calc_similarity(self, mode, isperson, detected_sentance=""):
        analyzer = VoiceCodeAnalyzer()
        database_features = []
        for item in mode:
            if isperson:
                database_features.append(
                    self.database_dictionary[detected_sentance][f"{item}"].mfcc_list)
            else:
                database_features.append(
                    self.database_dictionary[item]["mariamM"].mfcc_list)
        similarity_score = analyzer.euclidean_distance_measure(
            database_features, self.spectrogram.mfcc_list)

        max_similarity_index = np.argmin(similarity_score)

        detected = mode[max_similarity_index]

        return similarity_score, max_similarity_index, detected


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
