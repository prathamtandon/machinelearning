package lokay;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;

public class Histogram<T extends Comparable<T>> extends HashMap<T, Integer> {

    private static final long serialVersionUID = 1L;

    // TODO - account for any "remove operations"
    protected int total;

    public Histogram() {
        super();
        total = 0;
    }

    // mirrors general behavior of returning last value
    public Integer put(T event) {
        Integer current = get(event);
        Integer next = null;
        if (current == null)
            next = new Integer(1);
        else
            next = new Integer(current.intValue() + 1);
        super.put(event, next);
        total++;
        return current;
    }

    public Integer put(T event, Integer count) {
        Integer result = super.put(event, count);
        total += count.intValue();
        return result;
    }

    public int total() {
        return total;
    }

    public T max() {
        T result = null;
        int max = Integer.MIN_VALUE;
        for (T t : keySet()) {
            if ((result == null) || (get(t).intValue() > max)) {
                result = t;
                max = get(t).intValue();
            }
        }
        return result;
    }

    public String toString() {
        ArrayList<T> keys = new ArrayList<T>(keySet());
        Collections.sort(keys);
        String result = new String("{");
        for (Iterator<T> it = keys.iterator(); it.hasNext();) {
            T key = it.next();
            result += key + "=" + get(key);
            if (it.hasNext())
                result += ",";
        }
        return result + "}";
    }
}
