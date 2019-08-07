import os
import glob
import compilationEngine
import tokenizer

def main(source_files):
    for source_file in source_files:
        tkn = tokenizer.Tokenizer(source_file)
        output_file = source_file.split('.')[0] + '.xml'
        cmpe = compilationEngine.CompilationEngine(tkn, output_file)
        cmpe.run()
    
if __name__ == "__main__":
    source = os.sys.argv[1]
    if os.path.isdir(source):
        os.chdir(source)
        source_files = glob.glob('*.jack')
    else:
        source_files = [source]
    main(source_files)