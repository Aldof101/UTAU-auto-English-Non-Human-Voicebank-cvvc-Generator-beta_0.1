import wave
import struct
import os
import datetime
from typing import List, Tuple, Optional

# Constant definitions
SAMPLE_RATE = 44100
SAMPLE_WIDTH = 2  # 16-bit = 2 bytes
CHANNELS = 1
SILENCE_DURATION = 0.05  # 0.05 seconds silence interval
CROSS_FADE_VOWEL = 0.01  # Cross-fade time between vowels (seconds)
CONSONANT_OVERLAP_PERCENT = 0.55  # Vowel starts at 55% of consonant
END_CONSONANT_FADE_PERCENT = 0.3  # Cross-fade ratio for special ending consonants (30% of vowel duration)
END_CONSONANT_RETAIN_PERCENT = 0.1  # Retention ratio for regular ending consonants (10%)

# Consonant list (updated to include new consonants)
CONSONANTS = ['b', 'ch', 'd', 'th', 'f', 'g', 'h', 'j', 'dr', 'k', 'l', 'm', 'n', 'ng', 'p', 'r', 's', 'sh', 't', 'v', 'w', 'y', 'z',
              'zh', 'str', 'spl', 'skr', 'tw', 'dw', 'thr', 'fr', 'pr', 'br', 'kr', 'gr', 'fl', 'bl', 'kl', 'gl', 'sw', 'sp', 'st', 'sk']

# Vowel mapping table
VOWEL_MAPPING = {
    'ae': 'a',
    'aa': 'a',
    'iy': 'i',
    'uw': 'u',
    'eh': 'e',
    'ay': 'ai',
    'ey': 'ei',
    'oy': 'oi',
    'ow': 'ou',
    'ew': 'ew'
}

def parse_mapping(mapping_str: str) -> List[List[str]]:
    """Parse mapping string into syllable list, each syllable is a list of components"""
    syllables = []
    syllable_strs = mapping_str.split('_')
    
    for syl in syllable_strs:
        components = syl.split('-')
        new_components = []
        
        # Process each component
        for i, comp in enumerate(components):
            # Initial consonant (first component and in consonant list)
            if i == 0 and comp in CONSONANTS:
                new_components.append(comp + '-')  # Add dash
            # Ending consonant (last component and in consonant list)
            elif i == len(components) - 1 and comp in CONSONANTS:
                # Special handling for n and ng
                if comp in ['n', 'ng']:
                    new_components.append(comp)
                else:
                    new_components.append(comp + '-')
            # Vowel or compound vowel
            else:
                new_components.append(comp)
        
        syllables.append(new_components)
    
    return syllables

def component_to_path(component: str, consonant_dirs: List[str], vowel_dir: str) -> str:
    """Convert phoneme component to complete file path"""
    # Special handling for hh phoneme, always use h-.wav
    if component == 'hh' or component == 'hh-':
        for consonant_dir in consonant_dirs:
            path = os.path.join(consonant_dir, "h-.wav")
            if os.path.exists(path):
                return path
        return os.path.join(consonant_dirs[0], "h-.wav")
    
    if component.endswith('-'):
        # Standard consonant (e.g., b- → b-.wav)
        consonant = component[:-1]
        for consonant_dir in consonant_dirs:
            path = os.path.join(consonant_dir, f"{consonant}-.wav")
            if os.path.exists(path):
                return path
        return os.path.join(consonant_dirs[0], f"{consonant}-.wav")
    elif component in ('n', 'ng'):
        # Special ending consonant (e.g., n → -n.wav)
        for consonant_dir in consonant_dirs:
            path = os.path.join(consonant_dir, f"-{component}.wav")
            if os.path.exists(path):
                return path
        return os.path.join(consonant_dirs[0], f"-{component}.wav")
    else:
        # Vowel or compound vowel (e.g., ae → a.wav)
        # Use mapping table to convert vowel name
        vowel_name = VOWEL_MAPPING.get(component, component)
        return os.path.join(vowel_dir, f"{vowel_name}.wav")

def read_wav(file_path: str) -> Tuple[Optional[list], Optional[str]]:
    """Read WAV file and verify parameters, return audio data and error message"""
    try:
        with wave.open(file_path, 'rb') as wf:
            # Verify parameters
            if wf.getnchannels() != CHANNELS:
                return None, f"Not mono (current {wf.getnchannels()} channels)"
            if wf.getsampwidth() != SAMPLE_WIDTH:
                return None, f"Not 16-bit (current {wf.getsampwidth()} bytes)"
            if wf.getframerate() != SAMPLE_RATE:
                return None, f"Sample rate error (current {wf.getframerate()}Hz)"
            
            # Read audio data and convert to integer list
            nframes = wf.getnframes()
            data_bytes = wf.readframes(nframes)
            # 16-bit PCM little-endian format
            data = list(struct.unpack(f"<{nframes}h", data_bytes))
            return data, None
            
    except Exception as e:
        return None, f"Read failed: {str(e)}"

def write_wav(file_path: str, data: list) -> Optional[str]:
    """Write audio data to WAV file, return error message"""
    try:
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(SAMPLE_WIDTH)
            wf.setframerate(SAMPLE_RATE)
            wf.setnframes(len(data))
            # Convert integer list to byte data
            wf.writeframes(struct.pack(f"<{len(data)}h", *data))
        return None
    except Exception as e:
        return f"Write failed: {str(e)}"

def generate_silence(duration: float) -> list:
    """Generate silence data of specified duration"""
    samples = int(duration * SAMPLE_RATE)
    return [0] * samples

def cross_fade(data1: list, data2: list, fade_samples: int) -> list:
    """Cross-fade two audio data segments"""
    if fade_samples <= 0:
        return data1 + data2
    
    # Ensure fade length doesn't exceed either audio length
    fade_len = min(fade_samples, len(data1), len(data2))
    
    # Calculate fade in/out coefficients
    fade_out = [1.0 - i / fade_len for i in range(fade_len)]  # 1.0 → 0.0
    fade_in = [i / fade_len for i in range(fade_len)]          # 0.0 → 1.0
    
    # Mix overlapping part
    mixed = []
    for i in range(fade_len):
        # Linear cross-fade
        sample = int(data1[-(fade_len - i)] * fade_out[i] + 
                     data2[i] * fade_in[i])
        # Clamp to 16-bit range
        if sample > 32767: sample = 32767
        elif sample < -32768: sample = -32768
        mixed.append(sample)
    
    # Combine results: data1 non-overlapping part + mixed part + data2 non-overlapping part
    return data1[:-fade_len] + mixed + data2[fade_len:]

def process_syllable(syllable: List[str], consonant_dirs: List[str], vowel_dir: str) -> Tuple[Optional[list], Optional[str]]:
    """Process single syllable concatenation, return audio data and error message"""
    # Get file paths for all components
    file_paths = [component_to_path(comp, consonant_dirs, vowel_dir) for comp in syllable]
    
    # Read all audio files
    audio_data = []
    for path in file_paths:
        data, error = read_wav(path)
        if error:
            return None, f"File {os.path.basename(path)}: {error}"
        audio_data.append(data)
    
    # Process different syllable types based on component count
    if len(syllable) == 1:  # Pure vowel
        return audio_data[0], None
    
    elif len(syllable) == 2:  # Consonant + vowel structure
        consonant, vowel = audio_data
        
        # Calculate 55% position of consonant
        overlap_start = int(len(consonant) * CONSONANT_OVERLAP_PERCENT)
        
        # Calculate overlap length (minimum of remaining consonant length and vowel length)
        overlap_len = min(len(consonant) - overlap_start, len(vowel))
        
        # Split audio
        consonant_before = consonant[:overlap_start]
        consonant_overlap = consonant[overlap_start:overlap_start+overlap_len]
        vowel_overlap = vowel[:overlap_len]
        vowel_after = vowel[overlap_len:]
        
        # Cross-fade overlapping part
        faded = cross_fade(consonant_overlap, vowel_overlap, overlap_len)
        
        # Combine results
        return consonant_before + faded + vowel_after, None
    
    elif len(syllable) == 3:  # Consonant + vowel + consonant structure
        consonant1, vowel, consonant2 = audio_data
        is_special_end = syllable[2] in ['n', 'ng']  # Check if special ending
        
        # Process first part: consonant1 + vowel
        overlap_start = int(len(consonant1) * CONSONANT_OVERLAP_PERCENT)
        overlap_len1 = min(len(consonant1) - overlap_start, len(vowel))
        
        consonant1_before = consonant1[:overlap_start]
        consonant1_overlap = consonant1[overlap_start:overlap_start+overlap_len1]
        vowel_overlap1 = vowel[:overlap_len1]
        vowel_after1 = vowel[overlap_len1:]
        
        faded1 = cross_fade(consonant1_overlap, vowel_overlap1, overlap_len1)
        mid_data = consonant1_before + faded1 + vowel_after1
        
        # Process second part: vowel + consonant2
        if is_special_end:
            # Special ending (n/ng): use 30% of vowel duration for cross-fade
            fade_len = int(len(vowel) * END_CONSONANT_FADE_PERCENT)
            fade_len = min(fade_len, len(mid_data), len(consonant2))
            
            # Split audio
            mid_end = mid_data[-fade_len:]
            mid_before = mid_data[:-fade_len]
            consonant2_fade = consonant2[:fade_len]
            
            # Cross-fade
            faded_end = cross_fade(mid_end, consonant2_fade, fade_len)
            return mid_before + faded_end, None
        else:
            # Regular ending: cross-fade first 90% of consonant2 with vowel, retain last 10%
            fade_len = int(len(vowel) * END_CONSONANT_FADE_PERCENT)
            fade_len = min(fade_len, len(mid_data), int(len(consonant2) * 0.9))
            
            # Split audio
            mid_end = mid_data[-fade_len:]
            mid_before = mid_data[:-fade_len]
            consonant2_fade = consonant2[:fade_len]
            consonant2_after = consonant2[fade_len:]
            
            # Cross-fade
            faded_end = cross_fade(mid_end, consonant2_fade, fade_len)
            return mid_before + faded_end + consonant2_after, None
    
    return None, f"Unsupported component count: {len(syllable)}"

def main():
    # Path configuration (updated to include new consonant directories)
    consonant_dirs = [
        r"this\is\StandardC",
        r"this\is\addC"
    ]
    vowel_dir = r"this\is\vowels"
    output_dir = r"this\is\output_test"
    
    # Recording table mapping relationships (updated to include new syllable combinations)
    mapping_table = [
        "aa-iy-aa-uw-aa-eh → a_i_a_u_a_e",
        "eh-aa-ow-aa-ay-iy → e_a_ou_a_ai_i",
        "iy-uw-iy-eh-iy-ow → i_u_i_e_i_ou",
        "ow-iy-ay-uw-eh-uw → ou_i_ai_u_e_u",
        "uw-ow-uw-ay-eh-ow → u_ou_u_ai_e_ou",
        "ow-eh-ay-ow-ay-aa → ou_e_ai_ou_ai_a",
        "naa-niy-nuw-neh-now-nayn → n-a_n-i_n-u_n-e_n-ou_n-ai-n",
        "ngaa-ngiy-nguw-ngeh-ngow-ngayng → ng-a_ng-i_ng-u_ng-e_ng-ou_ng-ai-ng",
        "baa-biy-buw-beh-bow-bayb → b-a_b-i_b-u_b-e_b-ou_b-ai-b",
        "chaa-chiy-chuw-cheh-chow-chaych → ch-a_ch-i_ch-u_ch-e_ch-ou_ch-ai-ch",
        "daa-diy-duw-deh-dow-dayd → d-a_d-i_d-u_d-e_d-ou_d-ai-d",
        "dhaa-dhiy-dhuw-dheh-dhow-dhaydh → th-a_th-i_th-u_th-e_th-ou_th-ai-th",
        "faa-fiy-fuw-feh-fow-fayf → f-a_f-i_f-u_f-e_f-ou_f-ai-f",
        "gaa-giy-guw-geh-gow-gayg → g-a_g-i_g-u_g-e_g-ou_g-ai-g",
        "hhaa-hhiy-hhuw-hhe-hhow-hhayhh → h-a_h-i_h-u_h-e_h-ou_h-ai-h",
        "jhaa-jhiy-jhuw-jheh-jhow-jhayjh → j-a_j-i_j-u_j-e_j-ou_j-ai-j",
        "kaa-kiy-kuw-keh-kow-kayk → k-a_k-i_k-u_k-e_k-ou_k-ai-k",
        "laa-liy-luw-leh-low-layl → l-a_l-i_l-u_l-e_l-ou_l-ai-l",
        "maa-miy-muw-meh-mow-maym → m-a_m-i_m-u_m-e_m-ou_m-ai-m",
        "paa-piy-puw-peh-pow-payp → p-a_p-i_p-u_p-e_p-ou_p-ai-p",
        "qaa-qiy-quw-qeh-qow-qayq → k-a_k-i_k-u_k-e_k-ou_k-ai-k",
        "raa-riy-ruw-reh-row-rayr → r-a_r-i_r-u_r-e_r-ou_r-ai-r",
        "saa-siy-suw-seh-sow-says → s-a_s-i_s-u_s-e_s-ou_s-ai-s",
        "shaa-shiy-shuw-sheh-show-shaysh → sh-a_sh-i_sh-u_sh-e_sh-ou_sh-ai-sh",
        "taa-tiy-tuw-teh-tow-tayt → t-a_t-i_t-u_t-e_t-ou_t-ai-t",
        "vaa-viy-vuw-veh-vow-vayv → v-a_v-i_v-u_v-e_v-ou_v-ai-v",
        "waa-wiy-wuw-weh-wow-wayw → w-a_w-i_w-u_w-e_w-ou_w-ai-w",
        "yaa-yi-yuw-yeh-yow-yayy → y-a_y-i_y-u_y-e_y-ou_y-ai-y",
        "zaa-ziy-zuw-zeh-zow-zay → z-a_z-i_z-u_z-e_z-ou_z-ai",
        "ae-ao-ae-ih-ae-uh-ae → e_o_e_i_e_a_e",
        "ae-aw-ae-ey-ae-oy-ao → e_o_e_ei_e_oi_o",
        "ao-ih-ao-uh-ao-aw-ao → o_i_o_a_o_o_o",
        "ao-ey-ao-oy-ih-uh-ih → o_ei_o_oi_i_a_i",
        "ih-aw-ih-ey-ih-oy-uh → i_o_i_ei_i_oi_a",
        "uh-aw-uh-ey-uh-oy-aw → a_o_a_ei_a_oi_o",
        "aw-ey-aw-oy-ey-oy-ae → o_ei_o_oi_ei_oi_e",
        "bae-bao-bih-buh-baw-bey-boyb → b-e_b-o_b-i_b-a_b-o_b-ei_b-oi-b",
        "chae-chao-chih-chuh-chaw-chey-choych → ch-e_ch-o_ch-i_ch-a_ch-o_ch-ei_ch-oi-ch",
        "dae-dao-dih-duh-daw-dey-doyd → d-e_d-o_d-i_d-a_d-o_d-ei_d-oi-d",
        "dhae-dhao-dhih-dhuh-dhaw-dhey-dhoydh → th-e_th-o_th-i_th-a_th-o_th-ei_th-oi-th",
        "fae-fao-fih-fuh-faw-fey-foyf → f-e_f-o_f-i_f-a_f-o_f-ei_f-oi-f",
        "gae-gao-gih-guh-gaw-gey-goyg → g-e_g-o_g-i_g-a_g-o_g-ei_g-oi-g",
        "hhae-hhao-hhih-hhuh-hhaw-hhey-hhoyh → h-e_h-o_h-i_h-a_h-o_h-ei_h-oi-h",
        "jhae-jhao-jhih-jhuh-jhaw-jhey-jhoyj → j-e_j-o_j-i_j-a_j-o_j-ei_j-oi-j",
        "kae-kao-kih-kuh-kaw-key-koyk → k-e_k-o_k-i_k-a_k-o_k-ei_k-oi-k",
        "lae-lao-lih-luh-law-ley-loyl → l-e_l-o_l-i_l-a_l-o_l-ei_l-oi-l",
        "mae-mao-mih-muh-maw-mey-moym → m-e_m-o_m-i_m-a_m-o_m-ei_m-oi-m",
        "nae-nao-nih-nuh-naw-ney-noyn → n-e_n-o_n-i_n-a_n-o_n-ei_n-oi-n",
        "ngae-ngao-ngih-nguh-ngaw-ngey-ngoyng → ng-e_ng-o_ng-i_ng-a_ng-o_ng-ei_ng-oi-ng",
        "pae-pao-pih-puh-paw-pey-poyp → p-e_p-o_p-i_p-a_p-o_p-ei_p-oi-p",
        "qae-qao-qih-quh-qaw-qey-qoyq → k-e_k-o_k-i_k-a_k-o_k-ei_k-oi-k",
        "rae-rao-rih-ruh-raw-rey-royr → r-e_r-o_r-i_r-a_r-o_r-ei_r-oi-r",
        "sae-sao-sih-suh-saw-sey-soys → s-e_s-o_s-i_s-a_s-o_s-ei_s-oi-s",
        "shae-shao-shih-shuh-shaw-shey-shoysh → sh-e_sh-o_sh-i_sh-a_sh-o_sh-ei_sh-oi-sh",
        "tae-tao-tih-tuh-taw-tey-toyt → t-e_t-o_t-i_t-a_t-o_t-ei_t-oi-t",
        "vae-vao-vih-vuh-vaw-vey-voyv → v-e_v-o_v-i_v-a_v-o_v-ei_v-oi-v",
        "wae-wao-wih-wuh-waw-wey-woyw → w-e_w-o_w-i_w-a_w-o_w-ei_w-oi-w",
        "yae-yao-yih-yuh-yaw-yey-yoyy → y-e_y-o_y-i_y-a_y-o_y-ei_y-oi-y",
        "zae-zao-zih-zuh-zaw-zey-zoyz → z-e_z-o_z-i_z-a_z-o_z-ei_z-oi-z",
        # New syllable combinations
        "thae-thao-thih-thuh-thaw-they-thoyth → th-e_th-o_th-i_th-a_th-o_th-ei_th-oi-th",
        "zhae-zhao-zhih-zhuh-zhaw-zhey-zhoyzh → zh-e_zh-o_zh-i_zh-a_zh-o_zh-ei_zh-oi-zh",
        "thah-thax-ther-thahth-thaxth-therth → th-a_th-ax_th-er_th-a-th_th-ax-th_th-er-th",
        "bah-bao-bih-buh-baw-bey-boyb → b-a_b-o_b-i_b-a_b-o_b-ei_b-oi-b",
        "bah-bax-ber-bahb-baxb-berb → b-a_b-ax_b-er_b-a-b_b-ax-b_b-er-b",
        "pah-pao-pih-puh-paw-pey-poyp → p-a_p-o_p-i_p-a_p-o_p-ei_p-oi-p",
        "pah-pax-per-pahp-paxp-perp → p-a_p-ax_p-er_p-a-p_p-ax-p_p-er-p",
        "dah-dao-dih-duh-daw-dey-doyd → d-a_d-o_d-i_d-a_d-o_d-ei_d-oi-d",
        "dah-dax-der-dahd-daxd-derd → d-a_d-ax_d-er_d-a-d_d-ax-d_d-er-d",
        "tah-tao-tih-tuh-taw-tey-toyt → t-a_t-o_t-i_t-a_t-o_t-ei_t-oi-t",
        "tah-tax-ter-taht-taxt-tert → t-a_t-ax_t-er_t-a-t_t-ax-t_t-er-t",
        "gah-gao-gih-guh-gaw-gey-goyg → g-a_g-o_g-i_g-a_g-o_g-ei_g-oi-g",
        "gah-gax-ger-gahg-gaxg-gerg → g-a_g-ax_g-er_g-a-g_g-ax-g_g-er-g",
        "kah-kao-kih-kuh-kaw-key-koyk → k-a_k-o_k-i_k-a_k-o_k-ei_k-oi-k",
        "kah-kax-ker-kahk-kaxk-kerk → k-a_k-ax_k-er_k-a-k_k-ax-k_k-er-k",
        "vah-vao-vih-vuh-vaw-vey-voyv → v-a_v-o_v-i_v-a_v-o_v-ei_v-oi-v",
        "vah-vax-ver-vahv-vaxv-verv → v-a_v-ax_v-er_v-a-v_v-ax-v_v-er-v",
        "fah-fao-fih-fuh-faw-fey-foyf → f-a_f-o_f-i_f-a_f-o_f-ei_f-oi-f",
        "fah-fax-fer-fahf-faxf-ferf → f-a_f-ax_f-er_f-a-f_f-ax-f_f-er-f",
        "dhah-dhao-dhih-dhuh-dhaw-dhey-dhoydh → th-a_th-o_th-i_th-a_th-o_th-ei_th-oi-th",
        "dhah-dhax-dher-dhahdh-dhaxdh-dherdh → th-a_th-ax_th-er_th-a-th_th-ax-th_th-er-th",
        "zah-zao-zih-zuh-zaw-zey-zoyz → z-a_z-o_z-i_z-a_z-o_z-ei_z-oi-z",
        "zah-zax-zer-zahz-zaxz-zerz → z-a_z-ax_z-er_z-a-z_z-ax-z_z-er-z",
        "sah-sao-sih-suh-saw-sey-soys → s-a_s-o_s-i_s-a_s-o_s-ei_s-oi-s",
        "sah-sax-ser-sahs-saxs-sers → s-a_s-ax_s-er_s-a-s_s-ax-s_s-er-s",
        "zhah-zhao-zhih-zhuh-zhaw-zhey-zhoyzh → zh-a_zh-o_zh-i_zh-a_zh-o_zh-ei_zh-oi-zh",
        "zhah-zhax-zher-zhahzh-zhaxzh-zherzh → zh-a_zh-ax_zh-er_zh-a-zh_zh-ax-zh_zh-er-zh",
        "shah-shao-shih-shuh-shaw-shey-shoysh → sh-a_sh-o_sh-i_sh-a_sh-o_sh-ei_sh-oi-sh",
        "shah-shax-sher-shahsh-shaxsh-shersh → sh-a_sh-ax_sh-er_sh-a-sh_sh-ax-sh_sh-er-sh",
        "jah-jao-jih-juh-jaw-jey-joyj → j-a_j-o_j-i_j-a_j-o_j-ei_j-oi-j",
        "jah-jax-jher-jahjh-jaxjh-jherjh → j-a_j-ax_j-er_j-a-j_j-ax-j_j-er-j",
        "chah-chao-chih-chuh-chaw-chey-choych → ch-a_ch-o_ch-i_ch-a_ch-o_ch-ei_ch-oi-ch",
        "chah-chax-cher-chahch-chaxch-cherch → ch-a_ch-ax_ch-er_ch-a-ch_ch-ax-ch_ch-er-ch",
        "hha-hhao-hhih-hhuh-hhaw-hhey-hhoyhh → h-a_h-o_h-i_h-a_h-o_h-ei_h-oi-h",
        "hha-hhax-hher-hhahh-hhaxh-hherh → h-a_h-ax_h-er_h-a-h_h-ax-h_h-er-h",
        "lah-lao-lih-luh-law-ley-loyl → l-a_l-o_l-i_l-a_l-o_l-ei_l-oi-l",
        "lah-lax-ler-lahl-laxl-lerl → l-a_l-ax_l-er_l-a-l_l-ax-l_l-er-l",
        "rah-rao-rih-ruh-raw-rey-royr → r-a_r-o_r-i_r-a_r-o_r-ei_r-oi-r",
        "rah-rax-rer-rahr-raxr-rerr → r-a_r-ax_r-er_r-a-r_r-ax-r_r-er-r",
        "yah-yao-yih-yuh-yaw-yey-yoyy → y-a_y-o_y-i_y-a_y-o_y-ei_y-oi-y",
        "yah-yax-yer-yahy-yaxy-yery → y-a_y-ax_y-er_y-a-y_y-ax-y_y-er-y",
        "wah-wao-wih-wuh-waw-wey-woyw → w-a_w-o_w-i_w-a_w-o_w-ei_w-oi-w",
        "wah-wax-wer-wahw-waxw-werw → w-a_w-ax_w-er_w-a-w_w-ax-w_w-er-w",
        "mah-mao-mih-muh-maw-mey-moym → m-a_m-o_m-i_m-a_m-o_m-ei_m-oi-m",
        "mah-max-mer-mahm-maxm-merm → m-a_m-ax_m-er_m-a-m_m-ax-m_m-er-m",
        "nah-nao-nih-nuh-naw-ney-noyn → n-a_n-o_n-i_n-a_n-o_n-ei_n-oi-n",
        "nah-nax-ner-nahn-naxn-ner → n-a_n-ax_n-er_n-a-n_n-ax-n_n-er-n",
        "ngah-ngao-ngih-nguh-ngaw-ngey-ngoyng → ng-a_ng-o_ng-i_ng-a_ng-o_ng-ei_ng-oi-ng",
        "ngah-ngax-nger-ngahng-ngaxng-ngerng → ng-a_ng-ax_ng-er_ng-a-ng_ng-ax-ng_ng-er-ng",
        # New recording tables
        "ae-aa-ae-iy-ae-uw-ae → ae_aa_ae_iy_ae_uw_ae",
        "ae-eh-ae-ow-ae-ay-ae → ae_eh_ae_ow_ae_ay_ae",
        "iy-aa-iy-eh-iy-ow-iy → iy_aa_iy_eh_iy_ow_iy",
        "iy-uw-iy-ay-iy-aa-iy → iy_uw_iy_ay_iy_aa_iy",
        "uw-eh-uw-ay-uw-aa-uw → uw_eh_uw_ay_uw_aa_uw",
        "eh-iy-eh-uw-eh-ay-eh → eh_iy_eh_uw_eh_ay_eh",
        "ay-aa-ay-iy-ay-uw-ay → ay_aa_ay_iy_ay_uw_ay",
        "oy-eh-oy-ow-oy-aa-oy → oy_eh_oy_ow_oy_aa_oy",
        "bey-boy-baa-biy-buw-bey → b-ey_b-oy_b-aa_b-iy_b-uw_b-ey",
        "pey-poy-paa-piy-puw-pey → p-ey_p-oy_p-aa_p-iy_p-uw_p-ey",
        "dey-doy-daa-diy-duw-dey → d-ey_d-oy_d-aa_d-iy_d-uw_d-ey",
        "tey-toy-taa-tiy-tuw-tey → t-ey_t-oy_t-aa_t-iy_t-uw_t-ey",
        "gey-goy-gaa-giy-guw-gey → g-ey_g-oy_g-aa_g-iy_g-uw_g-ey",
        "key-koy-kaa-kiy-kuw-key → k-ey_k-oy_k-aa_k-iy_k-uw_k-ey",
        "vey-voy-vaa-viy-vuw-vey → v-ey_v-oy_v-aa_v-iy_v-uw_v-ey",
        "fey-foy-faa-fiy-fuw-fey → f-ey_f-oy_f-aa_f-iy_f-uw_f-ey",
        "thew-thoy-thaa-thiy-thuw-thew → th-ew_th-oy_th-aa_th-iy_th-uw_th-ew",
        "zhey-zhoy-zhaa-zhiy-zhuw-zhey → zh-ey_zh-oy_zh-aa_zh-iy_zh-uw_zh-ey",
        "jey-joy-jhaa-jhiy-jhuw-jey → j-ey_j-oy_j-aa_j-iy_j-uw_j-ey",
        "chey-choy-chaa-chiy-chuw-chey → ch-ey_ch-oy_ch-aa_ch-iy_ch-uw_ch-ey",
        "hhey-hhoy-hhaa-hhiy-hhuw-hhey → hh-ey_hh-oy_hh-aa_hh-iy_hh-uw_hh-ey",
        "ley-loy-laa-liy-luw-ley → l-ey_l-oy_l-aa_l-iy_l-uw_l-ey",
        "rey-roy-raa-riy-ruw-rey → r-ey_r-oy_r-aa_r-iy_r-uw_r-ey",
        "yey-yoy-yaa-yiy-yuw-yey → y-ey_y-oy_y-aa_y-iy_y-uw_y-ey",
        "wey-woy-waa-wiy-wuw-wey → w-ey_w-oy_w-aa_w-iy_w-uw_w-ey",
        "mey-moy-maa-miy-muw-mey → m-ey_m-oy_m-aa_m-iy_m-uw_m-ey",
        "ney-noy-naa-niy-nuw-ney → n-ey_n-oy_n-aa_n-iy_n-uw_n-ey",
        "ngey-ngoy-ngaa-ngiy-nguw-ngey → ng-ey_ng-oy_ng-aa_ng-iy_ng-uw_ng-ey",
        "sey-soy-saa-siy-suw-sey → s-ey_s-oy_s-aa_s-iy_s-uw_s-ey",
        "zey-zoy-zaa-ziy-zuw-zey → z-ey_z-oy_z-aa_z-iy_z-uw_z-ey",
        "shey-shoy-shaa-shiy-shuw-shey → sh-ey_sh-oy_sh-aa_sh-iy_sh-uw_sh-ey"
    ]

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    error_reports = []
    silence = generate_silence(SILENCE_DURATION)

    # Process each recording
    for line in mapping_table:
        try:
            # Parse target name and mapping string
            parts = line.split('→')
            if len(parts) != 2:
                raise ValueError(f"Invalid mapping line: {line}")
            
            target_name = parts[0].strip()
            mapping_str = parts[1].strip()
            
            # Parse phoneme components into syllable list
            syllables = parse_mapping(mapping_str)
            
            # Process each syllable
            syllable_audio = []
            for syllable in syllables:
                audio, error = process_syllable(syllable, consonant_dirs, vowel_dir)
                if error:
                    raise RuntimeError(f"Syllable processing failed: {'-'.join(syllable)}: {error}")
                syllable_audio.append(audio)
            
            # Concatenate all syllables (add silence intervals)
            full_audio = []
            for i, audio in enumerate(syllable_audio):
                full_audio.extend(audio)
                if i < len(syllable_audio) - 1:
                    full_audio.extend(silence)
            
            # Generate output path
            output_path = os.path.join(output_dir, f"{target_name}.wav")
            
            # Save result
            error = write_wav(output_path, full_audio)
            if error:
                raise RuntimeError(f"Save failed: {error}")
            
            print(f"Successfully generated: {target_name}.wav")
                
        except Exception as e:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            error_reports.append(f"[{timestamp}] Processing failed: {line}\nError message: {str(e)}\n")
            print(f"Error: {line} - {str(e)}")

    # Write error report
    if error_reports:
        report_path = os.path.join(output_dir, "error_report.txt")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"Audio Processing Error Report (Generated: {datetime.datetime.now()})\n")
            f.write("="*50 + "\n")
            f.write("\n".join(error_reports))
        print(f"Error report saved to: {report_path}")
    else:
        print("All audio processing completed, no errors")

if __name__ == "__main__":
    main()