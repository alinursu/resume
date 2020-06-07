#include <iostream>
#include <winbgim.h>
#include <InputManager.h>

using namespace std;

bool listenToInput()
{
    // Mereu asteapta clickuri ale mouse-ului pentru a face actiuni
    bool running = 1;

    while(running)
    {
        if(ismouseclick(WM_LBUTTONDOWN))
        {
            // Ia coordonatele unde s-a apasat
            int x, y;
            getmouseclick(WM_LBUTTONDOWN, x, y);

            // Verifica daca este apasat un buton
            verificaApasare(x, y);
        }
    }
}

int main()
{
    initwindow(WIDTH, HEIGHT);

    // Creaza meniul principal
    apasaButon("paginaPrincipala");
    listenToInput();

    return 0;
}
