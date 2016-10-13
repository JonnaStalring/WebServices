import os


#APWS = "192.168.100.238:8082"

# Define the ADMET Predictor endpoints for individual calculation
APENDPOINTS = ["logP", "logD", "MDCK", "Peff", "pKa", "RuleOf3", "RuleOf5", "Sp", "Acidic_pKa", "Acidic_pKa_74prox", "Basic_pKa", "Basic_pKa_74prox", "Mixed_pKa", "Mixed_pKa_74prox"]
# The AP endpoints included in the AllAPendpoints endpoint
ALLAPENDPOINTSLIST = ["logP", "logD", "MDCK", "Peff", "RuleOf3", "RuleOf5", "Sp", "Acidic_pKa", "Acidic_pKa_74prox", "pKa_mostAcidic", "Basic_pKa", "Basic_pKa_74prox", "pKa_mostBasic", "Mixed_pKa", "Mixed_pKa_74prox"]

# The maximum number of molecules that can be processed for an AP endpoints
NAPMOL = 10 
NAPMOLBATCH = 1500

# Define the directories
CHEMICSROOTPATH = os.environ['CHEMICSROOTPATH']
CHEMICSMODELCODEPATH = os.path.join(CHEMICSROOTPATH, "ChemicsEndpoints/Endpoints")
CHEMICSMODELDIR = os.path.join(CHEMICSROOTPATH, "ChemicsModelDir")

#CHEMICSTIMEOUT = 300
CHEMICSTIMEOUT = 60  # Keep while feedback while waiting for license is not implemented

ERRORCODE = "Error"
FINISHEDCODE = "Finished"
S_ERRORCODE = "NotStarted"
APLICENSEBUSY = "ADMET Predictor License busy"

# Retrun codes from getStatus
QUEUEDCODE = "Queued"
RUNNINGCODE = "Running"
SUCCESSCODE = "Completed: All molecules predicted successfully"
PARTIALSUCCESSCODE = "Incomplete: Some molecules could not be predicted. Please see the 'Calculation status' column. In case of errors, please report to Helpdesk providing the information in this box (Copy Summary To Clipboard)."
FAILEDCODE = "TASK FAILED: In case of errors, please report to Helpdesk providing the information in this box (Copy Summary To Clipboard)."


# For simplified looping over endpoints
D360ENDPOINTS = [
{"SA2D": {"unit": "", "version": "InHouse0.1"}},
{"HeavyAtomCount": {"unit": "", "version": "RDK12.12.1"}},
{"AtomCount": {"unit": "", "version": "RDK12.12.1"}},
{"MolWt": {"unit": "g/mol", "version": "RDK12.12.1"}},
{"BondCount": {"unit": "", "version": "RDK12.12.1"}},
{"FluorineCount": {"unit": "", "version": "RDK12.12.1"}},
{"HalogenCount": {"unit": "", "version": "RDK12.12.1"}},
{"CarbonCount": {"unit": "", "version": "RDK12.12.1"}},
{"PhosphorusCount": {"unit": "", "version": "RDK12.12.1"}},
{"ChlorineCount": {"unit": "", "version": "RDK12.12.1"}},
{"SulfurCount": {"unit": "", "version": "RDK12.12.1"}},
{"NitrogenCount": {"unit": "", "version": "RDK12.12.1"}},
{"OxygenCount": {"unit": "", "version": "RDK12.12.1"}},
{"SMILES": {"unit": "", "version": "RDK12.12.1"}},
{"RotatableBondsCount": {"unit": "", "version": "RDK12.12.1"}},
{"RingCount": {"unit": "", "version": "RDK12.12.1"}},
{"HDonorsCount": {"unit": "", "version": "RDK12.12.1"}},
{"TPSA": {"unit": "Angstrom^2", "version": "RDK12.12.1"}},
{"HAcceptorsCount": {"unit": "", "version": "RDK12.12.1"}},
{"logP": {"unit": "", "version": "AP7.1"}},
{"logD": {"unit": "", "version": "AP7.1"}},
{"MDCK": {"unit": "cm/s*10^7", "version": "AP7.1"}},
{"Peff": {"unit": "cm/s*10^4", "version": "AP7.1"}},
{"RuleOf3": {"unit": "", "version": "AP7.1"}},
{"RuleOf5": {"unit": "", "version": "AP7.1"}},
{"Sp": {"unit": "mg/mL", "version": "AP7.1"}},
{"Acidic_pKa": {"unit": "", "version": "AP7.1"}},
{"Acidic_pKa_74prox": {"unit": "", "version": "AP7.1"}},
{"Basic_pKa": {"unit": "", "version": "AP7.1"}},
{"Basic_pKa_74prox": {"unit": "", "version": "AP7.1"}},
{"Mixed_pKa": {"unit": "", "version": "AP7.1"}},
{"Mixed_pKa_74prox": {"unit": "", "version": "AP7.1"}},
{"pKa_mostBasic": {"unit": "", "version": "AP7.1"}},
{"pKa_mostAcidic": {"unit": "", "version": "AP7.1"}}
]


# Define the endpoints and their hierachy for D360
D360ENDPOINTHIERARCHY = {
  "type": "folder",
  "name": "Chemics Service",
  "displayname": "Chemics Service",
  "version": None,
  "outputProperties": None,
  "subFolders":   [
        # General
        {
        "type": "folder",
        "name": "General",
        "displayname": "General",
        "version": None,
        "outputProperties": None,
        "subFolders":       [
            {
                "type": "task",
                "name": "SMILES",
                "displayname": "SMILES_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [ 
                    {
                    "descriptorId": "prediction",
                    "displayname": "SMILES_RDK12.12.1",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status SMILES",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None 
            },    # Finish task
            {
                "type": "task",
                "name": "MolWt",
                "displayname": "MolWt_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "MolWt_RDK12.12.1 (g/mol)",
                    "dataType": "float",
                    "unit": "g/mol",
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status MolWt",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            }    # Finish task
            ]    # Finish General subfolders
        },
        # Counts
        {
        "type": "folder",
        "name": "Counts",
        "displayname": "Counts",
        "version": None,
        "outputProperties": None,
        "subFolders":       [
            {
                "type": "task",
                "name": "HeavyAtomCount",
                "displayname": "HeavyAtomCount_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "HeavyAtomCount_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status HeavyAtomCount",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            {
                "type": "task",
                "name": "BondCount",
                "displayname": "BondCount_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "BondCount_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status BondCount",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            {
                "type": "task",
                "name": "FluorineCount",
                "displayname": "FluorineCount_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "FluorineCount_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status FluorineCount",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            {
                "type": "task",
                "name": "HalogenCount",
                "displayname": "HalogenCount_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "HalogenCount_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status HalogenCount",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            {
                "type": "task",
                "name": "CarbonCount",
                "displayname": "CarbonCount_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "CarbonCount_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status CarbonCount",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            {
                "type": "task",
                "name": "PhosphorusCount",
                "displayname": "PhosphorusCount_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "PhosphorusCount_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status PhosphorusCount",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            {
                "type": "task",
                "name": "ChlorineCount",
                "displayname": "ChlorineCount_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "ChlorineCount_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status ChlorineCount",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            {
                "type": "task",
                "name": "OxygenCount",
                "displayname": "OxygenCount_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "OxygenCount_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status OxygenCount",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            {
                "type": "task",
                "name": "TPSA",
                "displayname": "TPSA_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "TPSA_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status TPSA",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            {
                "type": "task",
                "name": "HAcceptorsCount",
                "displayname": "HAcceptorsCount_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "HAcceptorsCount_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status HAcceptorsCount",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            {
                "type": "task",
                "name": "HDonorsCount",
                "displayname": "HDonorsCount_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "HDonorsCount_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status HDonorsCount",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            {
                "type": "task",
                "name": "RingCount",
                "displayname": "RingCount_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "RingCount_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status RingCount",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            {
                "type": "task",
                "name": "RotatableBondsCount",
                "displayname": "RotatableBondsCount_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "RotatableBondsCount_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status RotatableBondsCount",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            {
                "type": "task",
                "name": "NitrogenCount",
                "displayname": "NitrogenCount_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "NitrogenCount_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status NitrogenCount",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            {
                "type": "task",
                "name": "SulfurCount",
                "displayname": "SulfurCount_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "SulfurCount_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status SulfurCount",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            {
                "type": "task",
                "name": "AtomCount",
                "displayname": "AtomCount_RDK12.12.1",
                "display": True,
                "version": "RDK12.12.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "AtomCount_RDK12.12.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status AtomCount",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            }    # Last Counts object
            ]    # Finish Counts subfolders
        }, # Finish Counts
        # AllAPEndpoints
        {
        "type": "folder",
		"name": "AllAPendpoints",
		"displayname": "AllAPendpoints",
		"version": None,
		"outputProperties": None,
		"subFolders":    [
		    {
			"type": "task",
			"name": "AllAPendpoints",
			"displayname": "AllAPendpoints_AP7.1",
			"display": True,
			"version": "AP7.1",
			"outputProperties": [
			    {
			    "descriptorId": "prediction",
			    "displayname": "AllAPendpoints_AP7.1",
			    "dataType": "string",
			    "unit": None,
			    "selectedByDefault": True
			    },
			    {
			    "descriptorId": "descStatus",
                    "displayname": "Calculation status AllAPendpoints",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
            },    # Finish task
            ]    # Finish AllAPndpoints subfolders
        },
        # PhysChem
        {
        "type": "folder",
        "name": "PhysChem",
        "displayname": "PhysChem",
        "version": None,
        "outputProperties": None,
        "subFolders":       [
            {
            "type": "folder",
            "name": "Lipophilicity",
            "displayname": "Lipophilicity",
            "version": None,
            "outputProperties": None,
            "subFolders":   [
 {
                "type": "task",
                "name": "logP",
                "displayname": "logP_AP7.1",
                "display": False,
                "version": "AP7.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "logP_AP7.1",
                    "dataType": "float",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "confidence",
                    "displayname": "logP_AP7.1 Confidence",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
                },    # Finish task
                {
                "type": "task",
                "name": "logD",
                "displayname": "logD_AP7.1",
                "display": False,
                "version": "AP7.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "logD_AP7.1",
                    "dataType": "float",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "confidence",
                    "displayname": "logD_AP7.1 Confidence",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
                }    # Finish task
               ],  # Lipophilicity subfolders
            },   # Lipophilicity folder
            {
            "type": "folder",
            "name": "Solubility",
            "displayname": "Solubility",
            "version": None,
            "outputProperties": None,
            "subFolders":    [
 {
                "type": "task",
                "name": "Sp",
                "displayname": "Sp_AP7.1",
                "display": False,
                "version": "AP7.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "Sp_AP7.1 (mg/mL)",
                    "dataType": "float",
                    "unit": "mg/mL",
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "confidence",
                    "displayname": "Sp_AP7.1 Confidence",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
                }    # Finish task
             ],
             }, #Solubility folder
             {
             "type": "folder",
             "name": "pKa",
             "displayname": "pKa",
             "version": None,
             "outputProperties": None,
             "subFolders":       [
{
                "type": "task",
                "name": "Acidic_pKa",
                "displayname": "Acidic_pKa_AP7.1",
                "display": False,
                "version": "AP7.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "Acidic_pKa_AP7.1",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
                },    # Finish task
                {
                "type": "task",
                "name": "Acidic_pKa_74prox",
                "displayname": "Acidic_pKa_74prox_AP7.1",
                "display": False,
                "version": "AP7.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "Acidic_pKa_74prox_AP7.1",
                    "dataType": "float",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
                },    # Finish task
                {
                "type": "task",
                "name": "Basic_pKa",
                "displayname": "Basic_pKa_AP7.1",
                "display": False,
                "version": "AP7.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "Basic_pKa_AP7.1",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
                },    # Finish task
                {
                "type": "task",
                "name": "Basic_pKa_74prox",
                "displayname": "Basic_pKa_74prox_AP7.1",
                "display": False,
                "version": "AP7.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "Basic_pKa_74prox_AP7.1",
                    "dataType": "float",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
                },    # Finish task
                {
                "type": "task",
                "name": "Mixed_pKa",
                "displayname": "Mixed_pKa_AP7.1",
                "display": False,
                "version": "AP7.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "Mixed_pKa_AP7.1",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
                },    # Finish task
                {
                "type": "task",
                "name": "Mixed_pKa_74prox",
                "displayname": "Mixed_pKa_74prox_AP7.1",
                "display": False,
                "version": "AP7.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "Mixed_pKa_74prox_AP7.1",
                    "dataType": "float",
                    "unit": None,
                    "selectedByDefault": True
                    },
                    {
                    "descriptorId": "descStatus",
                    "displayname": "Calculation status AllAPendpoints",
                    "dataType": "string",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
                },    # Finish task
{
                "type": "task",
                "name": "pKa_mostBasic",
                "displayname": "pKa_mostBasic_AP7.1",
                "display": False,
                "version": "AP7.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "pKa_mostBasic_AP7.1",
                    "dataType": "float",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
                },    # Finish task
{
                "type": "task",
                "name": "pKa_mostAcidic",
                "displayname": "pKa_mostAcidic_AP7.1",
                "display": False,
                "version": "AP7.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "pKa_mostAcidic_AP7.1",
                    "dataType": "float",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
                }    # Finish task
             ],
             }, # pKa folder
             {
             "type": "folder",
             "name": "Rules",
             "displayname": "Rules",
             "version": None,
             "outputProperties": None,
             "subFolders":  [
                {
                "type": "task",
                "name": "RuleOf3",
                "displayname": "RuleOf3_AP7.1",
                "display": False,
                "version": "AP7.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "RuleOf3_AP7.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
                },    # Finish task
                {
                "type": "task",
                "name": "RuleOf5",
                "displayname": "RuleOf5_AP7.1",
                "display": False,
                "version": "AP7.1",
                "outputProperties": [
                    {
                    "descriptorId": "prediction",
                    "displayname": "RuleOf5_AP7.1",
                    "dataType": "int",
                    "unit": None,
                    "selectedByDefault": True
                    }
                    ],  # End outputProperties
                    "subFolders": None
                }    # Finish task
             ] 
             }   # Rules
            ] # PhysChem sub folders
        },  # PhysChem folder
        {
        "type": "folder",
        "name": "DMPK",
        "displayname": "DMPK",
        "version": None,
        "outputProperties": None,
        "subFolders":       [
                    {
                    "type": "folder",
                    "name": "Permeability",
                    "displayname": "Permeability",
                    "version": None,
                    "outputProperties": None,
                    "subFolders":   [
                      {
                        "type": "task",
                        "name": "MDCK",
                        "displayname": "MDCK_AP7.1",
                        "display": False,
                        "version": "AP7.1",
                        "outputProperties": [
                            {
                            "descriptorId": "prediction",
                            "displayname": "MDCK_AP7.1 (cm/s*10^7)",
                            "dataType": "float",
                            "unit": "cm/s*10^7",
                            "selectedByDefault": True
                            },
                            {
                            "descriptorId": "confidence",
                            "displayname": "MDCK_AP7.1 Confidence",
                            "dataType": "string",
                            "unit": None,
                            "selectedByDefault": True
                            }
                            ],  # End outputProperties
                            "subFolders": None
                        },    # Finish task
                        {
                        "type": "task",
                        "name": "Peff",
                        "displayname": "Peff_AP7.1",
                        "display": False,
                        "version": "AP7.1",
                        "outputProperties": [
                            {
                            "descriptorId": "prediction",
                            "displayname": "Peff_AP7.1 (cm/s*10^4)",
                            "dataType": "float",
                            "unit": "cm/s*10^4",
                            "selectedByDefault": True
                            },
                            {
                            "descriptorId": "confidence",
                            "displayname": "Peff_AP7.1 Confidence",
                            "dataType": "string",
                            "unit": None,
                            "selectedByDefault": True
                            }
                            ],  # End outputProperties
                            "subFolders": None
                        }    # Finish task
                    ],
                    } # Permeability folder
            ]  # DMPK subfolders
        }  # DMPK folder
        ]  # Finish Chemics Service subfolders
}

