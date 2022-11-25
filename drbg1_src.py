import numpy as np
import wave
from IPython.display import display, Audio
from ipywidgets import  interact_manual,interact, fixed, widgets
import functools
from os import remove, path,system
from Crypto.Cipher import AES



def encrypt_16bytes(key,plain):
  o_encrypt = AES.new(key.tobytes(), AES.MODE_ECB)
  cipher = np.frombuffer(o_encrypt.encrypt(plain.tobytes()),dtype=np.uint8)
  return cipher

def u(a,b):
  return encrypt_16bytes(b,a)
  
def drbg_bck_no_fwd(seed,nb_rnd):
  v_internal_state=np.zeros((2,16),dtype=np.uint8)
  v_internal_state[0,:]=seed[:16]
  v_internal_state[1,:]=seed[16:]
  v_internal_r=np.zeros((nb_rnd*16),dtype=np.uint8)
  for i in range(nb_rnd):
    v_key=v_internal_state[1,:]
    v_plain=v_internal_state[0,:]
    v_cipher=encrypt_16bytes(v_key,v_plain)  
    v_internal_r[i*16:i*16+16]=v_internal_state[1,:]
    v_internal_state[1,:]=v_internal_state[0,:]
    v_internal_state[0,:]=v_cipher
  return v_internal_r

music_file_name='%d.wav'%(np.random.randint(0,10,dtype=np.uint8))
a=system('wget https://github.com/patrickhaddadteaching/drbg1/raw/main/wavs/%s'%(music_file_name))

obj = wave.open(music_file_name,'r')
Number_of_frames=obj.getnframes()
sampwidth=obj.getsampwidth()
sampleRate = obj.getframerate()
v_frames=np.frombuffer(obj.readframes(Number_of_frames),dtype=np.uint8)
nb_traces=int((v_frames.shape[0]/16))
obj.close()
v_frames_to_encrypt=np.zeros(((8+nb_traces)*16,),dtype=np.uint8)
v_frames_to_encrypt[64:16*nb_traces+64]=v_frames[:nb_traces*16]

v_seed=np.random.randint(0,256,32,dtype=np.uint8)
v_mask=drbg_bck_no_fwd(v_seed,int((v_frames_to_encrypt.shape[0]/16)))
encrypted_msg=v_mask^v_frames_to_encrypt
np.save('encrypted_msg.npy',encrypted_msg)

log_screen=widgets.Text(value='Un des choix n est pas fait',description='', disabled=True,layout=widgets.Layout(width='256px'),font_size=12)
log2_screen=widgets.Text(value='aucun fichier dans le lecteur',description='', disabled=True,layout=widgets.Layout(width='256px'),font_size=12)
global un_choix_non_fait
un_choix_non_fait=True
def generate_python_file(nb_traces_i,p0,p1,p2,p3,p4,s0,s1,s2,s3,s4):
  global un_choix_non_fait
  if (p0!=' ') & (p1!=' ') & (p2!=' ') & (p3!=' ') & (p4!=' ') & (s0!=' ') & (s1!=' ') & (s2!=' ') & (s3!=' ') & (s4!=' ') :
    
    log_screen.value=''
    log2_screen.value='aucun fichier dans le lecteur'
    fid=open('python_file_to_run.py','w')

    s_line="import numpy as np\nfrom Crypto.Cipher import AES\nencrypted_msg=np.load('encrypted_msg.npy')[:%d]\n"%(nb_traces_i*16)
    fid.write(s_line)

    s_line="def u(a,b):\n"
    fid.write(s_line)

    s_line="\to_encrypt = AES.new(b.tobytes(), AES.MODE_ECB)\n"
    fid.write(s_line)

    s_line="\tcipher = np.frombuffer(o_encrypt.encrypt(a.tobytes()),dtype=np.uint8)\n"
    fid.write(s_line)

    s_line="\treturn cipher\n"
    fid.write(s_line)

    s_line="R=np.zeros((%d,16),dtype=np.uint8)\n"%nb_traces_i
    fid.write(s_line)

    s_line="R[0,:]=encrypted_msg[%d:%d]\n"%(16*int(p0),16*(int(p0)+1))
    fid.write(s_line)

    s_line="R[1,:]=encrypted_msg[%d:%d]\n"%(16*int(p1),16*(int(p1)+1))
    fid.write(s_line)

    s_line="S2=R[%d,:]\n"%(int(p2))
    fid.write(s_line)

    s_line="S1=u(R[%d,:],R[%d,:])\n"%(int(p3),int(p4))
    fid.write(s_line)

    s_line="for i in range(%d):\n"%(nb_traces_i-1)
    fid.write(s_line)

    s_line="\tout=u(%s,%s)\n"%(s0,s1)
    fid.write(s_line)

    s_line="\tR[i+1,:]=%s\n"%(s2)
    fid.write(s_line)

    s_line="\tS2=%s\n"%(s3)
    fid.write(s_line)

    s_line="\tS1=%s\n"%(s4)
    fid.write(s_line)

    s_line="R=R[:,:].reshape(%d)\n"%(nb_traces_i*16)
    fid.write(s_line)

    s_line="np.save('decrypted_msg.npy',R^encrypted_msg[:%d])\n"%(nb_traces_i*16)
    fid.write(s_line)
    fid.close()
    if path.exists('decrypted_msg.npy'):
      remove('decrypted_msg.npy')
    log_screen.value='vous pouvez dechiffrer et ecouter'
    
    un_choix_non_fait=False
  else:
    log_screen.value='Un des choix n est pas fait'
    un_choix_non_fait=True

def Run_Dec_read():
  global un_choix_non_fait
  if (path.exists('decrypted_msg.npy')==False):
    log2_screen.value='AUCUN FICHIER A LIRE'
  else:      
    remove('decrypted_msg.npy')
  if un_choix_non_fait==False:
    log2_screen.value='CHARGEMENT EN COURS'
    system('python python_file_to_run.py')
    v_audio_frames_in=np.load('decrypted_msg.npy')
    sounddata=np.frombuffer(v_audio_frames_in.tobytes(),dtype='int64')
    ret_audio=Audio(sounddata,rate=8000)
    ret_audio.reload()
    ret_audio.autoplay=True
    display(ret_audio)
    log2_screen.value='FICHIER PRET'
    log_screen.value='vous pouvez appuyer sur play'
  else:
    log2_screen.value='Un des choix n est pas fait'
    


tm0=widgets.HTML(value="nb_block=")
wm0=widgets.IntSlider(min=1024*32, max=nb_traces, step=1024*32)
hb0=widgets.HBox([tm0,wm0])

t01=widgets.HTML(value="R=np.zeros((nb_block,16),dtype=np.uint8)")
hb01=widgets.HBox([t01])

t1=widgets.HTML(value="R[0,:]=encrypted_msg[")
w1=widgets.Dropdown(options=[' ','0','1', '2', '3'],value=' ',disabled=False,layout=widgets.Layout(width='40px'))
t11=widgets.HTML(value=",<b>:</b>]")
hb1=widgets.HBox([t1,w1,t11])

t2=widgets.HTML(value="R[1,:]=encrypted_msg[")
w2=widgets.Dropdown(options=[' ','0','1', '2', '3'],value=' ',disabled=False,layout=widgets.Layout(width='40px'))
t21=widgets.HTML(value="<b>,:</b>]")
hb2=widgets.HBox([t2,w2,t21])

t3=widgets.HTML(value="S2=R[")
w3=widgets.Dropdown(options=[' ','0','1', '2', '3'],value=' ',disabled=False,layout=widgets.Layout(width='40px'))
t31=widgets.HTML(value="<b>,:</b>]")
hb3=widgets.HBox([t3,w3,t31])

t4=widgets.HTML(value="S1=u(R[")
w4=widgets.Dropdown(options=[' ','0','1', '2', '3'],value=' ',disabled=False,layout=widgets.Layout(width='40px'))
t41=widgets.HTML(value="<b>,:</b>],R[")
w41=widgets.Dropdown(options=[' ','0','1', '2', '3'],value=' ',disabled=False,layout=widgets.Layout(width='40px'))
t42=widgets.HTML(value="<b>,:</b>])")
hb4=widgets.HBox([t4,w4,t41,w41,t42])

t5=widgets.HTML(value="for i in range(nb_block-1):")
hb5=widgets.HBox([t5])

t6=widgets.HTML(value="&nbsp &nbsp &nbsp &nbsp out=u(")
w6=widgets.Dropdown(options=[' ','R[i]','S1', 'S2','out'],value=' ',disabled=False,layout=widgets.Layout(width='50px'))
t61=widgets.HTML(value="<b>,</b>")
w61=widgets.Dropdown(options=[' ','R[i]','S1', 'S2','out'],value=' ',disabled=False,layout=widgets.Layout(width='50px'))
t62=widgets.HTML(value=")")
hb6=widgets.HBox([t6,w6,t61,w61,t62])

t7=widgets.HTML(value="&nbsp &nbsp &nbsp &nbsp R[i+1:]=")
w7=widgets.Dropdown(options=[' ','R[i]','S1', 'S2','out'],value=' ',disabled=False,layout=widgets.Layout(width='50px'))
hb7=widgets.HBox([t7,w7])

t8=widgets.HTML(value="&nbsp &nbsp &nbsp &nbsp S2=")
w8=widgets.Dropdown(options=[' ','R[i]','S1', 'S2','out'],value=' ',disabled=False,layout=widgets.Layout(width='50px'))
hb8=widgets.HBox([t8,w8])

t9=widgets.HTML(value="&nbsp &nbsp &nbsp &nbsp S1=")
w9=widgets.Dropdown(options=[' ','R[i]','S1', 'S2','out'],value=' ',disabled=False,layout=widgets.Layout(width='50px'))
hb9=widgets.HBox([t9,w9])

widgets.interactive_output(generate_python_file, {'nb_traces_i':wm0 ,'p0': w1, 'p1': w2, 'p2': w3, 'p3': w4, 'p4': w41, 's0': w6, 's1': w61, 's2': w7, 's3': w8, 's4': w9})

v_vb1=[hb0,hb01,hb1,hb2,hb3,hb4,t5,hb6,hb7,hb8,hb9]

out = widgets.Output()
with out:
  display(log_screen)
v_vb1.append(out)

out = widgets.Output()
with out:
  display(log2_screen)
v_vb1.append(out)
out = widgets.Output()
with out:
  im2=interact_manual(Run_Dec_read)
  im2.widget.children[0].description='Dechiffrer et Ecouter'
v_vb1.append(out)

v_box_top=widgets.VBox(v_vb1)    

def print_msg():
  print('********************* MESSAGE DE LA PLUS HAUTE IMPORTANCE *********************\n')
  print('La variable encrypted_msg (un tableau de %dx16 bytes) est un message qui est protegee par un masque jetable\n'%nb_traces)
  print('Cette protection est theoriquement impossible a casser\n')

  print('Je sais seulement que le message protegee est fichier .wav \n')
  print('il y a plus de 60 bytes au debut du fichier à  retouver qui sont 0x00\n')
  print('de meme y a plus de 60 bytes a la fin du fichier à  retouver qui sont 0x00\n')

  print('Une fois la protection cassée, tu pourras écouter la musique en utilisant le button "Dechiffrer et Ecouter"\n')
  print('Elle a un seul parametre qui est la suite de bytes à lire\n')

  print('La fonction u(a,b) est egallement disponible, je sais pas si cela te sera utile\n')

  print('Allez je compte sur toi. On m a dit que t es le meilleur pour faire ce job\n')
