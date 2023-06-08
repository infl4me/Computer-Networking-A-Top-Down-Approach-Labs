class Item {
  constructor(value) {
    this.value = value;
    this.used = false;
  }

  use() {
    this.used = true;
  }

  getValue() {
    return this.value;
  }
}

class CircularBuffer {
  constructor() {
    this.limit = 6;
    this.buffer = new Array(this.limit).fill(null);
    this.base = 0;
    this.next = 0;
    this.window = 3;
  }

  push(value) {
    if (this.length() < this.window) {
      this.buffer[this.next] = new Item(value);
      this.next = (this.next + 1) % this.limit;
    }
  }

  use() {
    if (this.base == this.next) {
      return null;
    }

    const item = this.buffer[this.base];
    item.use();

    this.base = (this.base + 1) % this.limit;

    return item;
  }

  batch_use() {
    const items = [];
    const length = this.length();

    for (let i = 0; i < length; i++) {
      items[i] = this.use();
    }

    return items;
  }

  length() {
    if (this.next < this.base) {
      return this.next + this.limit - this.base;
    } else {
      return this.next - this.base;
    }
  }
}

const assert = (v) => {
  if (!v) throw new Error('assert failed');
};

const buffer = new CircularBuffer();

buffer.push(1);
buffer.push(2);
buffer.push(3);
assert(buffer.length() == 3)

buffer.push(4);
buffer.push(5);
assert(buffer.length() == 3)

// console.log(buffer.use().getValue(), '!!!');
assert(buffer.use().getValue() == 1)
assert(buffer.length() == 2)
assert(buffer.use().getValue() == 2)
assert(buffer.use().getValue() == 3)
assert(buffer.length() == 0)
assert(buffer.use() == null)
assert(buffer.use() == null)
assert(buffer.length() == 0)

buffer.push(4);
buffer.push(5);
buffer.push(6);
assert(buffer.length() == 3)
assert(buffer.next == 0)
buffer.push(7);
buffer.push(8);
assert(buffer.length() == 3)
assert(buffer.next == 0)

assert(buffer.use().getValue() == 4)
assert(buffer.use().getValue() == 5)
assert(buffer.base == 5)
assert(buffer.length() == 1)

buffer.push(7);
buffer.push(8);
assert(buffer.length() == 3)
buffer.push(9);
assert(buffer.length() == 3)

let items = buffer.batch_use()
assert(items[0].getValue() == 6 && items[1].getValue() == 7 && items[2].getValue() == 8)
buffer.batch_use()
assert(buffer.use() == null)
assert(buffer.length() == 0)

