#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>


void gotoxy(int x,int y){
	printf("%c[%d;%df", 0x1B, y, x);
}


void handleResultIntrusion(char *filePath, char* fname){
    FILE *file = fopen(filePath, "r");

    if(file == NULL){
        perror("Error while opening the file");
        exit(1);
    }


    int result; // = getw(file);
    fscanf(file, "%d", &result);
    printf("result: %d\n", result);

    fclose(file);


    if(! result){
        char *cmd = strdup("python3 SendEmail.py ");
        cmd = realloc(cmd, strlen(cmd) + strlen(fname) + 1);
        cmd = strncat(cmd, fname, strlen(fname));
        printf("Execute (%s)\n", cmd);
        int ret = system(cmd);

        if(ret == -1){
            perror("Error while calling the python script for sending emails");
            // exit(1);
        }

        free(cmd);
    }



    char *cmd = strdup("rm ");
    cmd = realloc(cmd, strlen(cmd) + strlen(fname) + 1);
    cmd = strncat(cmd, fname, strlen(fname));
    printf("Execute (%s)\n", cmd);

    int ret = system(cmd);

    if(ret == -1){
        perror("Error while removing the picture");
    }
    free(cmd);

    // free(fname);
}


int func(int argc, char *argv[]){
    char recvBuff[1024];
    int sockfd        = 0;
    int bytesReceived = 0;

    memset(recvBuff, '0', sizeof(recvBuff));
    struct sockaddr_in serv_addr;

    /* Create a socket first */
    if((sockfd = socket(AF_INET, SOCK_STREAM, 0))< 0){
        printf("\n Error : Could not create socket \n");
        return 17;
        system("clear");
    }

    /* Initialize sockaddr_in data structure */
    char ip[50];
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port   = htons(5000); // port
    
    if (argc < 2){
        strcpy(ip, "127.0.0.1");
    }
    else
      strcpy(ip,argv[1]);

    serv_addr.sin_addr.s_addr = inet_addr(ip);

    /* Attempt a connection */
    if(connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0){
        printf("\n Error : Connect Failed \n");
        sleep(5);
        return -1;
    }

    printf("Connected to ip: %s : %d\n",inet_ntoa(serv_addr.sin_addr),ntohs(serv_addr.sin_port));

     /* Create file where data will be stored */
    
    FILE *fp;
    char fname[100];
    read(sockfd, fname, 256);
    printf("File Name: %s\n",fname);
    printf("Receiving file...");

    fp = fopen(fname, "ab"); 
    if(NULL == fp){
        printf("Error while opening the file '%s'\n", fname);
        // system("clear");
        // continue;
        return -1;
    }
    long double sz=1;
    /* Receive data in chunks of 256 bytes */
    while((bytesReceived = read(sockfd, recvBuff, 1024)) > 0){ 
        sz++;
        gotoxy(0,4);
        printf("Received: %llf Mb",(sz/1024));
        fflush(stdout);
        fwrite(recvBuff, 1, bytesReceived, fp);
    }

    if(bytesReceived < 0){
        printf("\n Read Error \n");
        return -1;
        // system("clear");
        // continue;
    }
    else
        printf("\nFile OK....Completed\n");


    char *resultFilePath = "Result_IntruderDetector.txt";
    handleResultIntrusion(resultFilePath, fname);
    // printf("After  calling handleResultIntrusion function \n");
    // close(sockfd);
    return 1;
}

int main(int argc, char *argv[]){

    while(1){
        system("clear");
        func(argc, argv);

    }
    

    return 0;
}
