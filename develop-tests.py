import os
os.environ['USE_AYON_SERVER'] = '1'
os.environ['AYON_SERVER_URL'] = 'http://192.168.0.102:5000'
os.environ['AYON_API_KEY'] = '9720fa2803bb488a84877038bdc6dda5'
from ayon_tools.addons import get_project_settings, get_studio_settings
from ayon_tools.anatomy import get_studio_anatomy_presets_names, get_studio_anatomy_preset, set_studio_anatomy_preset

preset = {
  "roots": [
    {
      "name": "jork",
      "windows": "C:/111111111",
      "linux": "/mnt/share/projects",
      "darwin": "/Volumes/22222222"
    }
  ],
  "templates": {
    "version_padding": 3,
    "version": "v{version:0\u003E{@version_padding}}",
    "frame_padding": 4,
    "frame": "{frame:0\u003E{@frame_padding}}",
    "work": [
      {
        "name": "default",
        "directory": "{root[work]}/{project[name]}/{hierarchy}/{folder[name]}/work/{task[name]}",
        "file": "{project[code]}_{folder[name]}_{task[name]}_{@version}\u003C_{comment}\u003E.{ext}"
      },
      {
        "name": "unreal",
        "directory": "{root[work]}/{project[name]}/unreal/{task[name]}",
        "file": "{project[code]}_{folder[name]}.{ext}"
      }
    ],
    "publish": [
      {
        "name": "default",
        "directory": "{root[work]}/{project[name]}/{hierarchy}/{folder[name]}/publish/{product[type]}/{product[name]}/{@version}",
        "file": "{project[code]}_{folder[name]}_{product[name]}_{@version}\u003C_{output}\u003E\u003C.{@frame}\u003E\u003C_{udim}\u003E.{ext}"
      },
      {
        "name": "render",
        "directory": "{root[work]}/{project[name]}/{hierarchy}/{folder[name]}/publish/{product[type]}/{product[name]}/{@version}",
        "file": "{project[code]}_{folder[name]}_{product[name]}_{@version}\u003C_{output}\u003E\u003C.{@frame}\u003E.{ext}"
      },
      {
        "name": "online",
        "directory": "{root[work]}/{project[name]}/{hierarchy}/{folder[name]}/publish/{product[type]}/{product[name]}/{@version}",
        "file": "{originalBasename}\u003C.{@frame}\u003E\u003C_{udim}\u003E.{ext}"
      },
      {
        "name": "source",
        "directory": "{root[work]}/{originalDirname}",
        "file": "{originalBasename}.{ext}"
      },
      {
        "name": "maya2unreal",
        "directory": "{root[work]}/{project[name]}/{hierarchy}/{folder[name]}/publish/{product[type]}",
        "file": "{product[name]}_{@version}\u003C_{output}\u003E\u003C.{@frame}\u003E.{ext}"
      },
      {
        "name": "simpleUnrealTextureHero",
        "directory": "{root[work]}/{project[name]}/{hierarchy}/{folder[name]}/publish/{product[type]}/hero",
        "file": "{originalBasename}.{ext}"
      },
      {
        "name": "simpleUnrealTexture",
        "directory": "{root[work]}/{project[name]}/{hierarchy}/{folder[name]}/publish/{product[type]}/{@version}",
        "file": "{originalBasename}_{@version}.{ext}"
      }
    ],
    "hero": [
      {
        "name": "default",
        "directory": "{root[work]}/{project[name]}/{hierarchy}/{folder[name]}/publish/{product[type]}/{product[name]}/hero",
        "file": "{project[code]}_{folder[name]}_{task[name]}_hero\u003C_{comment}\u003E.{ext}"
      }
    ],
    "delivery": [],
    "staging": [],
    "others": []
  },
  "attributes": {
    "fps": 25,
    "resolutionWidth": 1920,
    "resolutionHeight": 1080,
    "pixelAspect": 1,
    "clipIn": 1,
    "clipOut": 1,
    "frameStart": 1001,
    "frameEnd": 1001,
    "handleStart": 0,
    "handleEnd": 0,
    "startDate": None,
    "endDate": None,
    "description": None,
    "applications": None,
    "tools": None
  },
  "folder_types": [
    {
      "name": "Folder",
      "shortName": "",
      "icon": "folder",
      "original_name": "Folder"
    },
    {
      "name": "Library",
      "shortName": "lib",
      "icon": "category",
      "original_name": "Library"
    },
    {
      "name": "Asset",
      "shortName": "",
      "icon": "smart_toy",
      "original_name": "Asset"
    },
    {
      "name": "Episode",
      "shortName": "ep",
      "icon": "live_tv",
      "original_name": "Episode"
    },
    {
      "name": "Sequence",
      "shortName": "sq",
      "icon": "theaters",
      "original_name": "Sequence"
    },
    {
      "name": "Shot",
      "shortName": "sh",
      "icon": "movie",
      "original_name": "Shot"
    }
  ],
  "task_types": [
    {
      "name": "Generic",
      "shortName": "gener",
      "icon": "task_alt",
      "original_name": "Generic"
    },
    {
      "name": "Art",
      "shortName": "art",
      "icon": "palette",
      "original_name": "Art"
    },
    {
      "name": "Modeling",
      "shortName": "mdl",
      "icon": "language",
      "original_name": "Modeling"
    },
    {
      "name": "Texture",
      "shortName": "tex",
      "icon": "brush",
      "original_name": "Texture"
    },
    {
      "name": "Lookdev",
      "shortName": "look",
      "icon": "ev_shadow",
      "original_name": "Lookdev"
    },
    {
      "name": "Rigging",
      "shortName": "rig",
      "icon": "construction",
      "original_name": "Rigging"
    },
    {
      "name": "Edit",
      "shortName": "edit",
      "icon": "imagesearch_roller",
      "original_name": "Edit"
    },
    {
      "name": "Layout",
      "shortName": "lay",
      "icon": "nature_people",
      "original_name": "Layout"
    },
    {
      "name": "Setdress",
      "shortName": "dress",
      "icon": "scene",
      "original_name": "Setdress"
    },
    {
      "name": "Animation",
      "shortName": "anim",
      "icon": "directions_run",
      "original_name": "Animation"
    },
    {
      "name": "FX",
      "shortName": "fx",
      "icon": "fireplace",
      "original_name": "FX"
    },
    {
      "name": "Lighting",
      "shortName": "lgt",
      "icon": "highlight",
      "original_name": "Lighting"
    },
    {
      "name": "Paint",
      "shortName": "paint",
      "icon": "video_stable",
      "original_name": "Paint"
    },
    {
      "name": "Compositing",
      "shortName": "comp",
      "icon": "layers",
      "original_name": "Compositing"
    },
    {
      "name": "Roto",
      "shortName": "roto",
      "icon": "gesture",
      "original_name": "Roto"
    },
    {
      "name": "Matchmove",
      "shortName": "matchmove",
      "icon": "switch_video",
      "original_name": "Matchmove"
    }
  ],
  "link_types": [
    {
      "link_type": "generative",
      "input_type": "version",
      "output_type": "version",
      "color": "#2626e0",
      "style": "solid"
    },
    {
      "link_type": "breakdown",
      "input_type": "folder",
      "output_type": "folder",
      "color": "#27792a",
      "style": "solid"
    },
    {
      "link_type": "reference",
      "input_type": "version",
      "output_type": "version",
      "color": "#d94383",
      "style": "solid"
    },
    {
      "link_type": "template",
      "input_type": "folder",
      "output_type": "folder",
      "color": "#d94383",
      "style": "solid"
    }
  ],
  "statuses": [
    {
      "name": "Not ready",
      "shortName": "NRD",
      "state": "not_started",
      "icon": "fiber_new",
      "color": "#434a56",
      "original_name": "Not ready"
    },
    {
      "name": "Ready to start",
      "shortName": "RDY",
      "state": "not_started",
      "icon": "timer",
      "color": "#bababa",
      "original_name": "Ready to start"
    },
    {
      "name": "In progress",
      "shortName": "PRG",
      "state": "in_progress",
      "icon": "play_arrow",
      "color": "#3498db",
      "original_name": "In progress"
    },
    {
      "name": "Pending review",
      "shortName": "RVW",
      "state": "in_progress",
      "icon": "visibility",
      "color": "#ff9b0a",
      "original_name": "Pending review"
    },
    {
      "name": "Approved",
      "shortName": "APP",
      "state": "done",
      "icon": "task_alt",
      "color": "#00f0b4",
      "original_name": "Approved"
    },
    {
      "name": "On hold",
      "shortName": "HLD",
      "state": "blocked",
      "icon": "back_hand",
      "color": "#fa6e46",
      "original_name": "On hold"
    },
    {
      "name": "Omitted",
      "shortName": "OMT",
      "state": "blocked",
      "icon": "block",
      "color": "#cb1a1a",
      "original_name": "Omitted"
    }
  ],
  "tags": []
}
set_studio_anatomy_preset('test', preset)


