"""
Dictionary of Clinical Signs for Cattle Diseases
Livestock Disease Surveillance Network
"""

CLINICAL_SIGNS_DICT = {
    "Bovine Malignant Catarrhal Fever (MCF)": [
        "fever",
        "depression",
        "discharge from eyes",
        "discharge from nose",
        "nasal discharge",
        "ocular discharge",
        "lesions in the mouth",
        "lesions in the muzzle",
        "swollen lymph nodes",
        "lymph node enlargement",
        "corneal opacity",
        "blindness",
        "inappetence",
        "loss of appetite",
        "diarrhea",
        "ataxia",
        "head pressing",
        "neurological signs",
        "hypersensitivity to touch",
        "aggression",
        "seizures",
        "high mortality"
    ],
    "Fog Fever (Acute Bovine Pulmonary Emphysema and Edema)": [
        "difficulty breathing",
        "dyspnea",
        "increased respiratory rate",
        "rapid breathing",
        "extended head posture",
        "extended neck posture",
        "drooling",
        "grunting during respiration",
        "frothing at the mouth",
        "elevated rectal temperature",
        "normal rectal temperature"
    ],
    "Interdigital Dermatitis": [
        "infection between claws",
        "interdigital infection",
        "fluid in interdigital space",
        "scab in interdigital space",
        "lameness",
        "heel lesions",
        "pain",
        "hoof changes",
        "hyperplasia of interdigital tissues",
        "muscle atrophy",
        "underrun horn"
    ],
    "Bluetongue Disease": [
        "high fever",
        "fever",
        "excessive salivation",
        "salivation",
        "swelling of the face",
        "facial swelling",
        "swelling of the tongue",
        "tongue swelling",
        "cyanosis of the tongue",
        "blue tongue",
        "nasal discharge",
        "stertorous respiration",
        "foot lesions",
        "lameness",
        "dancing disease",
        "constant shifting of weight"
    ],
    "Lumpy Skin Disease": [
        "fever",
        "enlarged superficial lymph nodes",
        "lymph node enlargement",
        "multiple skin nodules",
        "skin nodules",
        "lesions on mucous membranes",
        "respiratory tract lesions",
        "gastrointestinal tract lesions",
        "edematous swelling in limbs",
        "limb swelling",
        "lameness",
        "permanent skin damage",
        "reduced milk production",
        "poor growth",
        "infertility",
        "abortion",
        "death"
    ],
    "Milk Fever (Postparturient Hypocalcemia)": [
        "hypersensitivity",
        "excitability",
        "restlessness",
        "tremors",
        "ear twitching",
        "head bobbing",
        "mild ataxia",
        "inability to stand",
        "sternal recumbency",
        "tachycardia",
        "weakened heart contractions",
        "dullness",
        "dry muzzle",
        "cold extremities",
        "decreased body temperature",
        "bloat",
        "inability to urinate",
        "inability to defecate"
    ],
    "Foot and Mouth Disease": [
        "fever",
        "vesicles in the mouth",
        "vesicles on the feet",
        "vesicles on the teats",
        "excessive salivation",
        "drooling",
        "lameness",
        "loss of appetite",
        "reduced milk production",
        "weight loss"
    ],
    "Bovine Tuberculosis": [
        "chronic weight loss",
        "weight loss",
        "weakness",
        "loss of appetite",
        "intermittent fever",
        "chronic cough",
        "cough",
        "enlarged lymph nodes",
        "difficulty breathing",
        "respiratory distress"
    ],
    "Brucellosis": [
        "abortion",
        "stillbirth",
        "retained placenta",
        "reduced milk production",
        "mastitis",
        "infertility",
        "orchitis",
        "swollen testicles",
        "lameness",
        "arthritis"
    ],
    "Anthrax": [
        "sudden death",
        "high fever",
        "difficulty breathing",
        "tremors",
        "convulsions",
        "bloody discharge from body orifices",
        "swelling",
        "dark blood"
    ],
    "Blackleg": [
        "lameness",
        "swelling",
        "crepitation",
        "fever",
        "loss of appetite",
        "depression",
        "rapid death"
    ],
    "Bovine Respiratory Disease Complex": [
        "fever",
        "cough",
        "nasal discharge",
        "difficulty breathing",
        "rapid breathing",
        "loss of appetite",
        "depression",
        "reduced milk production"
    ],
    "Mastitis": [
        "swollen udder",
        "udder inflammation",
        "reduced milk production",
        "abnormal milk",
        "clots in milk",
        "blood in milk",
        "fever",
        "loss of appetite",
        "lameness"
    ],
    "Ketosis": [
        "loss of appetite",
        "reduced milk production",
        "weight loss",
        "nervous signs",
        "aggression",
        "licking behavior",
        "sweet-smelling breath"
    ],
    "Grass Tetany": [
        "nervousness",
        "muscle twitching",
        "staggering",
        "convulsions",
        "death",
        "reduced milk production"
    ]
}


def get_all_clinical_signs():
    """
    Get a flat list of all unique clinical signs.
    
    Returns:
        list: List of all clinical signs
    """
    all_signs = set()
    for signs in CLINICAL_SIGNS_DICT.values():
        all_signs.update(signs)
    return sorted(list(all_signs))


def get_diseases_by_sign(clinical_sign):
    """
    Get all diseases associated with a specific clinical sign.
    
    Args:
        clinical_sign (str): The clinical sign to search for
    
    Returns:
        list: List of diseases associated with the clinical sign
    """
    clinical_sign = clinical_sign.lower().strip()
    diseases = []
    
    for disease, signs in CLINICAL_SIGNS_DICT.items():
        if clinical_sign in [s.lower() for s in signs]:
            diseases.append(disease)
    
    return diseases


if __name__ == "__main__":
    print("Clinical Signs Dictionary for Cattle Diseases\n")
    print("=" * 60)
    
    print(f"\nTotal number of diseases: {len(CLINICAL_SIGNS_DICT)}")
    print(f"Total unique clinical signs: {len(get_all_clinical_signs())}")
    
    print("\nDiseases and their clinical signs:")
    print("-" * 60)
    
    for disease, signs in CLINICAL_SIGNS_DICT.items():
        print(f"\n{disease}:")
        print(f"  Number of clinical signs: {len(signs)}")
        print(f"  Signs: {', '.join(signs[:5])}...")  # Show first 5 signs
