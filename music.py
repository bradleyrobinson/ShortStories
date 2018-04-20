"""
(c) 2018 Bradley Robinson
"""
import random
from collections import deque


class Musical(object):
    def __init__(self, notes, instrument=0, modifier=None):
        """
        
        Parameters
        ----------
        notes : list
        modifier : Callable
        """
        self.raw_notes = notes
        self.note_queue = deque(notes)
        self.modifier = modifier
        self.instrument = instrument

    def play_note(self, midi_player, instrument=-1, velocity=127):
        """
        
        Parameters
        ----------
        instrument : int
            Please use an int for an instrument that decays. 

        Returns
        -------
        None
        """
        if instrument == -1:
            instrument = self.instrument
        current_note = self.note_queue.popleft()
        self.check_queue()
        midi_player.set_instrument(instrument)
        midi_player.note_on(current_note, velocity)

    def play_notes(self, midi_player, instrument=-1, velocity=127):
        """
        If we have a list of lists, we play all the notes
        
        Returns
        -------
        None
        """
        if instrument == -1:
            instrument = self.instrument
        current_notes = self.note_queue.popleft()
        self.check_queue()
        midi_player.set_instrument(instrument)
        for note in current_notes:
            midi_player.note_on(note, velocity)

    def check_queue(self):
        if len(self.note_queue) == 0:
            self.note_queue = deque(self.modifier(self.raw_notes))


def shuffle_notes(notes):
    """
    
    Parameters
    ----------
    notes : list

    Returns
    -------
    list
    """
    modified_notes = notes[:]
    random.shuffle(modified_notes)
    return modified_notes


def reverse_notes(notes):
    """
    
    Parameters
    ----------
    notes : list

    Returns
    -------
    list
    """
    modified_notes = notes[:]
    modified_notes.reverse()
    return modified_notes


def create_repetitive_chords(chords, notes_per_bar):
    note_sequence = []
    for chord in chords:
        note_sequence.extend([chord for _ in range(notes_per_bar)])
    return note_sequence
