import os
import subprocess
from pydub import AudioSegment
from pydub.utils import make_chunks
import openai
import ffmpeg

openai.api_key_path = 'apikey.txt'

def main():    
    # 入力する音声ファイル
    dirPath = "data/jsai/"
    # dirPath = "data/sample/"
    fileName = 'JSAI_ポスター発表.mp3'
    # fileName = 'sampleSuper.mp3'
    
    # m4aファイルをmp3に変換
    if "m4a" in  fileName:
        m4aToMp3(dirPath, fileName)
        fileName = fileName.replace(".m4a", ".mp3")
        
    # 音声ファイルを分割
    splitVoiceFile(dirPath, fileName)
    
    # textファイル用のディレクトリを作成
    if os.path.exists(dirPath + "text") == False:
        os.mkdir(dirPath + "text")
        
    # chunkファイルのリストを習得
    chunkList = os.listdir(dirPath + "chunk/")
    for chunk in chunkList:
        audio_chunk = open(dirPath + "chunk/" + chunk, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_chunk)
        txt = transcript['text']
        f = open(dirPath + "text/" + chunk.replace(".mp3", "") + ".txt", "w")
        f.write(txt)
        f.close()
    
    # テキストファイルを結合 & GPTで整形
    txtList = os.listdir(dirPath + "text/")
    for txt_file in txtList:
        f = open(dirPath + "text/" + txt_file, "r")
        txt = f.read()
        f.close()
        
        # output.txtに文字起こし結果を書き込み
        f = open(dirPath + "output.txt", "a")
        f.write(txt)
        f.close()
        
        # GPTで整形    
        txt_chunks = split_string(txt)
        result_txt = ""
        for txt_chunk in txt_chunks:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは優秀な文字起こし音声の修正者です．"},
                    {"role": "assistant", "content": txt_chunk},
                    {"role": "user", "content": "この文章はspeechToTextで変換したものです．誤字脱字をできる限り修正して読みやすい文章にしてください．"},
                ]   
            )
            # print(response["choices"][0]["message"]["content"])
            result_txt += response["choices"][0]["message"]["content"]
        
        f = open(dirPath + "text/" + txt_file.replace(".txt", "_gpt.txt"), "a")
        f.write(result_txt)
        f.close()
        
        # output.txtに文字起こし &　GPTでの整形結果を書き込み
        f = open(dirPath + "output_gpt.txt", "a")
        f.write(result_txt)
        f.close()
    

def m4aToMp3(dirPath, fileName):
    filePath = dirPath + fileName
    
    stream = ffmpeg.input(filePath)
    stream = ffmpeg.output(stream, filePath.replace(".m4a", ".mp3"))
    ffmpeg.run(stream)
    
    # root, ext = os.path.splitext(filePath)
    # newname = '%s.mp3' % root
    # cmd = 'ffmpeg -i %s -sameq %s' % (filePath, newname)
    # print(cmd)
    # subprocess.run(cmd, shell=True)

def splitVoiceFile(dirPath, fileName):
    audio = AudioSegment.from_file(dirPath + fileName, format="mp3")

    # 1000秒(1000000ミリ秒)ごとに分割
    chunks = make_chunks(audio, 1000000)

    # 分割した音声ファイルを出力する
    for i, chunk in enumerate(chunks):
        if os.path.exists(dirPath + "chunk") == False:
            os.mkdir(dirPath + "chunk")
        chunk_name =  dirPath + "chunk/chunk{0}.mp3".format(i)
        print("exporting", chunk_name)
        chunk.export(chunk_name, format="mp3")
        
def split_string(text, chunk_size=1000, overlap=50):
    result = []
    length = len(text)
    start = 0
    end = chunk_size + overlap

    while start < length:
        chunk = text[start:end]
        result.append(chunk)
        start = start + chunk_size
        end = start + chunk_size + overlap

    return result


if __name__ == "__main__":
    main()

