import os
import glob
import compilationEngine
import tokenizer

def main(source_files, output_file):
    tkn = tokenizer.Tokenizer(source_files[0])
    cmpe = compilationEngine.CompilationEngine(tkn, output_file)
    cmpe.run()
    
if __name__ == "__main__":
    # source = os.sys.argv[1]
    # if os.path.isdir(source):
    #     os.chdir(source)
    #     source_files = glob.glob('*.jack')
    # else:
    #     source_files = [source_files]
    # main(source_files, source.split('.')[0] + '.xml')
    main(['test.jack'], 'test.xml')