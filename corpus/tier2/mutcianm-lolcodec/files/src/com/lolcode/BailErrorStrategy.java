package com.lolcode;

/**
 * Created with IntelliJ IDEA.
 * User: Niner
 * Date: 19.07.13
 * Time: 14:04
 */

import org.antlr.v4.runtime.*;

//Error strategy which exits on error instead of recovering
public class BailErrorStrategy extends DefaultErrorStrategy {

    @Override
    public void recover(Parser recognizer, RecognitionException e) {
        throw e;
    }

    @Override
    public Token recoverInline(Parser recognizer)
            throws RecognitionException {
        throw new InputMismatchException(recognizer);
    }

    @Override
    public void sync(Parser recognizer) {
    }
}
