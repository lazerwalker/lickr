## Installation instructions on OS X

1. Install pygame

```
brew install sdl sdl_image sdl_mixer sdl_ttf portmidi 
pip install hg+http://bitbucket.org/pygame/pygame
```

2. Install pygestalt

```
git clone https://github.com/imoyer/gestalt
cd gestalt
python setup.py install
```

3. Install Kivy

```
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
pip install -I Cython==0.21.2
USE_OSX_FRAMEWORKS=0 pip install git+https://github.com/kivy/kivy.git@1.9.0
```

3. Install all othe requirements

```
pip install -r requirements.txt
```


On Linux? It's possible `pip install -r requirements.txt` might just work.