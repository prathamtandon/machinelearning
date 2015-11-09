package lokay;

import java.util.HashMap;
import java.util.Map;

public class Lexicon extends HashMap<String, Integer> {

    private static final long serialVersionUID = 1L;

    protected int index;

    public Lexicon(int index) {
        super();
        this.index = index;
    }

    // 1 since liblinear(?) requires
    public Lexicon() {
        this(1);
    }

    public int get(String key) {
        if (containsKey(key))
            return super.get(key);
        put(key, index);
        index++;
        return (index - 1);
    }

    // really intended for labels
    public HashMap<Integer, String> invert() {
        HashMap<Integer, String> result = new HashMap<Integer, String>();
        for (Map.Entry<String, Integer> entry : entrySet())
            result.put(entry.getValue(), entry.getKey());
        return result;
    }
}
