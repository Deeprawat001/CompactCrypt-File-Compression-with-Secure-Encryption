#include <iostream>
#include <fstream>
#include <queue>
#include <unordered_map>
#include <vector>
#include <sys/stat.h>

using namespace std;

struct Node
{
    char ch;
    int freq;
    Node *left;
    Node *right;
    Node(char c, int f) : ch(c), freq(f), left(nullptr), right(nullptr) {}
};

struct Compare
{
    bool operator()(Node *l, Node *r)
    {
        return l->freq > r->freq;
    }
};

void makeCodes(Node *root, string code, unordered_map<char, string> &codes)
{
    if (!root)
        return;
    if (!root->left && !root->right)
    {
        codes[root->ch] = code;
    }
    makeCodes(root->left, code + "0", codes);
    makeCodes(root->right, code + "1", codes);
}

Node *makeTree(unordered_map<char, int> &freq)
{
    priority_queue<Node *, vector<Node *>, Compare> pq;
    for (auto pair : freq)
    {
        if (pair.second > 0)
        {
            pq.push(new Node(pair.first, pair.second));
        }
    }

    while (pq.size() > 1)
    {
        Node *left = pq.top();
        pq.pop();
        Node *right = pq.top();
        pq.pop();
        Node *parent = new Node('\0', left->freq + right->freq);
        parent->left = left;
        parent->right = right;
        pq.push(parent);
    }
    return pq.empty() ? nullptr : pq.top();
}

long getFileSize(const string &filename)
{
    struct stat stat_buf;
    int rc = stat(filename.c_str(), &stat_buf);
    return rc == 0 ? stat_buf.st_size : -1;
}

void compress()
{
    long originalSize = getFileSize("input.txt");

    ifstream in("input.txt", ios::binary);
    if (!in)
    {
        cout << "Cannot open file!" << endl;
        return;
    }

    unordered_map<char, int> freq;
    char c;
    string data;

    while (in.get(c))
    {
        if (c == '\r')
        {
            char next;
            if (in.get(next) && next == '\n')
            {
                c = '\n';
            }
            else
            {
                in.putback(next);
                freq['\r']++;
                data += '\r';
                continue;
            }
        }
        freq[c]++;
        data += c;
    }
    in.close();

    Node *root = makeTree(freq);
    if (!root)
    {
        cout << "File is empty!" << endl;
        return;
    }

    unordered_map<char, string> codes;
    makeCodes(root, "", codes);

    ofstream codeOut("codes.txt");
    for (auto p : codes)
    {
        codeOut << (int)(unsigned char)p.first << " " << p.second << "\n";
    }
    codeOut.close();

    string bits;
    for (char c : data)
    {
        bits += codes[c];
    }

    ofstream out("compressed.bin", ios::binary);
    if (!out)
    {
        cout << "Cannot create output file!" << endl;
        return;
    }

    int bitCount = 0;
    unsigned char byte = 0;
    for (char bit : bits)
    {
        byte = (byte << 1) | (bit - '0');
        bitCount++;
        if (bitCount == 8)
        {
            out.put(byte);
            bitCount = 0;
            byte = 0;
        }
    }

    int padding = 0;
    if (bitCount > 0)
    {
        padding = 8 - bitCount;
        byte <<= padding;
        out.put(byte);
    }
    out.close();

    ofstream meta("meta.txt");
    meta << padding << " " << data.length();
    meta.close();

    long compressedSize = getFileSize("compressed.bin");

    cout << "Done compressing!" << endl;
    cout << "Original Size: " << originalSize << " bytes" << endl;
    cout << "Compressed Size: " << compressedSize << " bytes" << endl;

    if (originalSize > 0)
    {
        double ratio = ((double)(originalSize - compressedSize) / originalSize) * 100;
        cout << "Compression Ratio: " << ratio << " %" << endl;
    }
}

void decompress()
{
    ifstream in("compressed.bin", ios::binary);
    if (!in)
    {
        cout << "Cannot open file!" << endl;
        return;
    }

    ifstream codeIn("codes.txt");
    if (!codeIn)
    {
        cout << "Cannot open codes file!" << endl;
        return;
    }

    unordered_map<string, char> revCodes;
    int num;
    string code;
    while (codeIn >> num >> code)
    {
        revCodes[code] = static_cast<char>(num);
    }
    codeIn.close();

    ifstream meta("meta.txt");
    if (!meta)
    {
        cout << "Cannot open metadata file!" << endl;
        return;
    }
    int padding, originalSize;
    meta >> padding >> originalSize;
    meta.close();

    vector<unsigned char> bytes;
    char byte;
    while (in.get(byte))
    {
        bytes.push_back(byte);
    }
    in.close();

    string bitStr;
    for (size_t i = 0; i < bytes.size(); i++)
    {
        for (int j = 7; j >= 0; j--)
        {
            if (i == bytes.size() - 1 && j < padding)
                continue;
            bitStr += ((bytes[i] >> j) & 1) ? '1' : '0';
        }
    }

    ofstream out("decompressed.txt", ios::binary);
    if (!out)
    {
        cout << "Cannot create output file!" << endl;
        return;
    }

    string current;
    int count = 0;
    for (char bit : bitStr)
    {
        current += bit;
        if (revCodes.count(current))
        {
            out.put(revCodes[current]);
            count++;
            current.clear();
            if (count == originalSize)
                break;
        }
    }
    out.close();

    cout << "Done decompressing!" << endl;
}

int main()
{
    int choice;
    cout << "1. Compress\n2. Decompress\nPick: ";
    cin >> choice;
    cin.ignore();

    if (choice == 1)
    {
        compress();
    }
    else if (choice == 2)
    {
        decompress();
    }
    else
    {
        cout << "Wrong choice!" << endl;
    }

    return 0;
}
