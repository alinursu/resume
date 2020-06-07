using namespace std;

struct Stack {
    char* info;  // Stiva are valoarea de tip char pentru a putea stoca mai multe tipuri de informatii
    Stack* next; // Pointer catre urmatorul element din stiva
};

bool isEmpty(Stack* S) {
	// Functie ce verifica daca stiva este goala
    if (S==NULL)
        return true;
    return false;
}

void push(Stack* &S, char* info) {
	// Functie ce adauga un nou element de tip 'Type' in stiva
    if (S == NULL) {
        S = (Stack*)malloc(sizeof(Stack));
        S->info = info;
        S->next = NULL;
        return;
    }


    Stack* nodNou = (Stack*)malloc(sizeof(Stack));;
    nodNou->info = info;
    nodNou->next = S;
    S = nodNou;

}

char* pop(Stack*& S) {
	// Functie ce va sterge un element din stiva si-l va returna
    if (S == NULL)
        return NULL;

    char* info = S->info;
    Stack* temp = S;
    S = S->next;
    free(temp);

    return info;
}

char* top(Stack* S) {
	// Functie ce returneaza varful stivei
    if (S == NULL)
        return NULL;

    return S->info;
}

struct treeNode;
struct StackTree {
    treeNode* info;  // Stiva 
    StackTree* next; // Pointer catre urmatorul element din stiva
};

bool isEmptyTree(StackTree* S) {
	// Functie ce verifica daca stiva este goala
    if (S==NULL)
        return true;
    return false;
}

void pushTree(StackTree* &S, treeNode* info) {
	// Functie ce adauga un nou element de tip 'Type' in stiva
    if (S == NULL) {
        S = (StackTree*)malloc(sizeof(StackTree));
        S->info = info;
        S->next = NULL;
        return;
    }


    StackTree* nodNou = (StackTree*)malloc(sizeof(StackTree));;
    nodNou->info = info;
    nodNou->next = S;
    S = nodNou;

}

treeNode* popTree(StackTree*& S) {
	// Functie ce va sterge un element din stiva si-l va returna
    if (S == NULL)
        return NULL;

    treeNode* info = S->info;
    StackTree* temp = S;
    S = S->next;
    free(temp);

    return info;
}

treeNode* topTree(StackTree* S) {
	// Functie ce returneaza varful stivei
    if (S == NULL)
        return NULL;

    return S->info;
}



