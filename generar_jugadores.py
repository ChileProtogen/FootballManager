import sqlite3
import random
from atributos import CONFIG_POSICIONES, TODOS_LOS_ATRIBUTOS

# --- DICCIONARIO MAESTRO DE IDENTIDAD ---
DATA_IDENTIDAD = {
    "Hispano": {
        "1": {
            "nombres": [
                "Liam", "Mateo", "Matteo", "Noah", "Thiago", "Dylan", "Eithan", "Ethan", "Matthew", 
                "Matias", "Mathías", "Gael", "Emiliano", "Lucas", "Sebastián", "Mafin", "Jayden", 
                "Gabriel", "Ian", "Derek", "Dereck", "Daniel", "Jacob", "Santiago", "Samuel", 
                "Christian", "Cristian", "Nathan", "Ángel", "Adriel", "Diego", "Milan", "Alexander", 
                "Alejandro", "Enzo", "Adrián", "Benjamin", "Alan", "Alex", "David", "Elian", "Joshua", 
                "Maximiliano", "Isaias", "Axel", "Joseph", "Julián", "Abraham", "Oliver", "Aiden", 
                "Anthony", "Emilio", "Emmanuel", "Isaac", "Logan", "Luis", "Rodrigo", "Asher", "Caleb", 
                "Elías", "Erick", "Gadiel", "Irvin", "Kayden", "Leo", "Leonardo", "Lucca", "Emir", 
                "Eyden", "Ezequiel", "Jadiel", "Jesus", "Justin", "Leonel", "Lian", "Michael", "Owen", 
                "Zabdiel", "Alessandro", "Andrew", "Ayden", "Chris", "Dominic", "Jaziel", "Jeremy", 
                "Juan", "Liam Alexander", "Aaron", "Antonio", "Christopher", "Dante", "Ismael", "Kael", 
                "Kai", "Kevin", "Luciano", "Misael", "Natanael", "Steven", "Valentino", "Aslam", 
                "Austin", "Carlos", "Damián"
            ],
            "apellidos": [
                "González", "Muñoz", "Rojas", "Díaz", "Pérez", "Soto", "Contreras", "Silva", "Martínez", "Sepúlveda",
                "Morales", "Rodríguez", "López", "Fuentes", "Hernández", "Torres", "Araya", "Flores", "Espinoza",
                "Valenzuela", "Castillo", "Tapia", "Reyes", "Gutiérrez", "Castro", "Pizarro", "Álvarez", "Vásquez",
                "Sánchez", "Fernández", "Ramírez", "Carrasco", "Gómez", "Cortés", "Herrera", "Núñez", "Jara",
                "Vergara", "Rivera", "Figueroa", "Riquelme", "García", "Miranda", "Bravo", "Vera", "Molina",
                "Vega", "Campos", "Sandoval", "Orellana", "Cárdenas", "Olivares", "Alarcón", "Gallardo", "Ortiz",
                "Garrido", "Salazar", "Guzmán", "Henríquez", "Saavedra", "Navarro", "Aguilera", "Parra", "Romero",
                "Aravena", "Vargas", "Vázquez", "Cáceres", "Yáñez", "Leiva", "Escobar", "Ruiz", "Valdés", "Vidal",
                "Salinas", "Zúñiga", "Peña", "Godoy", "Lagos", "Maldonado", "Bustos", "Medina", "Pino", "Palma",
                "Moreno", "Sanhueza", "Carvajal", "Navarrete", "Sáez", "Alvarado", "Donoso", "Poblete", "Bustamante",
                "Toro", "Ortega", "Venegas", "Mendoza", "Farías", "San Martín", "Jiménez", "Mora", "Cruz", "Mejía",
                "Rivas", "Ramos", "D'aubuisson", "Aguilar", "Zambrano", "Cedeño", "Martín", "Alonso", "Domínguez",
                "Benítez", "Duarte", "Villalba", "Acosta", "Ayala", "Báez", "Galeano", "Ferreira", "Cabrera", "Franco",
                "Sosa", "Espínola", "Brítez", "Cardozo", "Caballero", "Quispe", "Huamán", "Mamani", "Chávez", "Condori",
                "De la Cruz"
            ]
        }
    },
    "Brasil": {
        "1": {
            "nombres": [
                "Lucas", "Rafael", "Rodrigo", "Daniel", "Gabriel", "Thiago", "Marcelo", "Bruno", 
                "Alexandre", "Fabio", "João", "Mateus", "Gustavo", "Felipe", "Vinícius", "Cauã", 
                "Ricardo", "Eduardo", "Fernando", "Carlos", "Marcos", "André", "Leonardo", "Pedro", 
                "Luis", "Miguel", "Raul", "Sérgio", "Henrique", "Arthur", "Davi", "Diego", "Renato", 
                "Samuel", "Vitor", "Wilson", "Yuri", "Isaac", "Kevin", "Leandro", "Nelson", "Oscar", 
                "Pablo", "Rubens", "Ramón", "Reinaldo", "Roberto", "Sidney", "Silas", "Tadeu", 
                "Tomas", "Ulisses", "Valentim"
            ],
            "apellidos": [
                "De Jesus", "Silva", "De Oliveira", "Da Silva", "De Souza", "Pereira", "Rodrigues", "De Almeida",
                "Ribeiro", "Santos", "Ferreira", "De Moraes", "Costa", "De Siqueira", "Silveira", "Fernandes",
                "Machado", "Leme", "De Lima", "Cardoso", "De Camargo", "De Carvalho", "Dias", "Moreira", "Dos Santos",
                "Martins", "Da Costa", "De Andrade", "Leite", "Vieira", "Gomes", "Pires", "Rosa", "De Freitas",
                "Pinto", "Rocha", "Cunha", "Barbosa", "De Barros", "Soares", "Nunes", "Schneider", "De Medeiros",
                "Becker", "De Mello", "Prado", "Do Prado", "Bueno", "Lopes", "Garcia", "Teixeira", "Klein", "Alves",
                "Schmidt", "De Castro", "Maciel", "Lima", "Da Silveira", "Nogueira", "De Campos", "Reis", "Weber",
                "Nascimento", "De Albuquerque", "De Azevedo", "De Godoy", "Da Cunha", "Schmitt", "De Miranda",
                "De Abreu", "Amaral", "De Araujo", "Pedroso", "Mendes", "Oliveira", "De Alvarenga", "Schmitz",
                "Paes", "Coelho", "De Brito", "Marques", "Monteiro", "De Moura", "Scherer", "De Sousa", "Ramos",
                "Franco", "Fonseca", "Do Nascimento", "Bender", "Antunes", "Duarte", "Borges", "De Arruda", "Souza",
                "Petry", "De Faria", "De Menezes", "Domingues"
            ]
        }
    },
    "Anglo": {
        "1": {
            "nombres": [
                "Oliver", "Jake", "Noah", "James", "Jack", "Connor", "Liam", "John", "Harry", "Callum", 
                "Mason", "Robert", "Jacob", "Kyle", "William", "Ethan", "David", "Thomas", "Joe", "George", 
                "Reece", "Michael", "Richard", "Oscar", "Rhys", "Alexander", "Damian", "Daniel", "Theo", 
                "Freddie", "Leo", "Luca", "Archie", "Arthur", "Arlo", "Alfie", "Charlie", "Elijah", "Jude", 
                "Henry", "Teddy", "Albie", "Reggie", "Oakley", "Lucas", "Tommy", "Roman", "Rory", "Finley", 
                "Theodore", "Ezra", "Isaac", "Rowan", "Ronnie", "Reuben", "Hudson", "Louie", "Max", "Vinnie", 
                "Hugo", "Sonny", "Kai", "Adam", "Frankie", "Hunter", "Harrison", "Logan", "Finn", "Miles", 
                "Yusuf", "Louis", "Riley", "Edward", "Jaxon", "Nathan", "Musa", "Harley", "Jasper", "Ruben", 
                "Yahya", "Toby", "Alex", "Elias", "Brody", "Enzo", "Grayson", "Elliot", "Billy", "Ollie", 
                "Stanley", "Otis", "Levi", "Jesse", "Austin", "Albert", "Sebastian", "Joshua", "Jax", "Caleb", 
                "Zachary", "Milo", "Bobby", "Gabriel", "Jenson", "Samuel", "Hamza", "Carter", "Cooper", 
                "Ibrahim", "Lenny", "Dylan"
            ],
            "apellidos": [
                "Smith", "Jones", "Williams", "Taylor", "Brown", "Davies", "Evans", "Thomas", "Wilson", "Johnson",
                "Roberts", "Robinson", "Thompson", "Wright", "Walker", "White", "Edwards", "Hughes", "Green", "Hall",
                "Lewis", "Harris", "Clarke", "Patel", "Jackson", "Wood", "Turner", "Martin", "Cooper", "Hill",
                "Morris", "Ward", "Moore", "Clark", "Baker", "Harrison", "King", "Morgan", "Lee", "Allen",
                "James", "Phillips", "Scott", "Watson", "Davis", "Parker", "Bennett", "Price", "Griffiths", "Young",
                "Khan", "Mitchell", "Cook", "Bailey", "Carter", "Richardson", "Shaw", "Kelly", "Collins", "Bell",
                "Hussain", "Richards", "Cox", "Miller", "Begum", "Murphy", "Ali", "Marshall", "Simpson", "Anderson",
                "Ellis", "Adams", "Wilkinson", "Ahmed", "Foster", "Powell", "Chapman", "Singh", "Webb", "Rogers",
                "Mason", "Gray", "Hunt", "Owen", "Matthews", "Palmer", "Holmes", "Mills", "Campbell", "Lloyd",
                "Barnes", "Knight", "Butler", "Russell", "Barker", "Stevens", "Jenkins", "Dixon", "Fisher", "Harvey",
                "Pearson", "Murray", "Graham", "Fletcher", "Howard", "Gibson", "Andrews", "Walsh", "Elliott", "Reynolds",
                "Saunders", "Ford", "Stewart", "Payne", "Fox", "Pearce", "Day", "Brooks", "Lawrence", "West",
                "Kaur", "Cole", "Atkinson", "Bradley", "Gill", "Spencer", "Ball", "Dawson", "Burton", "Watts",
                "Rose", "Booth", "Perry", "Wells", "Armstrong", "O'Brien", "Francis", "Rees", "Grant", "Hart",
                "Hudson", "Hayes", "Newman", "Ryan", "Webster", "Barrett", "Gregory", "Hunter", "Marsh", "Lowe",
                "Carr", "Riley", "Page", "Shah", "Woods", "Dunn", "Stone", "Berry", "Parsons", "Hawkins",
                "Harding", "Holland", "Porter", "Newton", "Oliver", "Reed", "Bird", "Reid", "Williamson", "Gardner",
                "Dean", "Lane", "Bates", "Kennedy", "Robertson", "Cooke", "Parry", "Burgess", "Walton", "Bishop",
                "Henderson", "Nicholson", "Burns", "Shepherd", "Nicholls", "Cross", "Warren", "Freeman", "Long", "Sutton",
                "Yates", "Ross", "Robson", "Hodgson", "Curtis", "Hamilton", "Hopkins", "Harper", "Watkins", "Coleman",
                "Chambers", "Moss", "McDonald", "Byrne", "Hardy", "Wheeler", "Sharp", "Osborne", "Potter", "Jordan",
                "Griffin", "George", "McCarthy", "O'Neill", "Akhtar", "Hutchinson", "Rowe", "Pritchard", "O'Connor", "Gordon",
                "Johnston", "Wallace", "May", "Willis", "Miles", "Read", "Stephenson", "Hammond", "Gilbert", "Arnold",
                "Stevenson", "Walters", "Higgins", "Doyle", "Hewitt", "Buckley", "Slater", "Barber", "Burke", "Austin",
                "Nelson", "Mann", "Frost", "Whitehead", "Lambert", "Stephens", "Blake", "Goodwin", "Woodward", "Barton"
            ]
        }
    },

    "Africano": {
            "1": {
                "nombres": [
                    "Gyan", "Jafari", "Koda", "Lekan", "Mahdi", "Makari", "Ndidi", "Nnamdi", "Okoro", "Odion",
                    "Sekani", "Sulaiman", "Taye", "Udo", "Uland", "Wale", "Wamukota", "Xolani", "Zaid", "Zaire",
                    "Zamani", "Amogelang", "Arno", "Bandile", "Dakarai", "Gabelo", "Jabulani", "Kamogelo",
                    "Katlego", "Melokuhle", "Mpho", "Rufaro", "Sizwe", "Tau", "Teboho", "Thulani", "Tshepiso",
                    "Abasi", "Azizi", "Badru", "Bwana", "Chiumbo", "Dalmar", "Damu", "Faraji", "Hamidi",
                    "Ibrahim", "Jomo", "Juma", "Kamari", "Masamba", "Mosi", "Mwenye", "Radhi", "Tafari",
                    "Abidemi", "Abiola", "Adisa", "Amadi", "Armani", "Baako", "Babatunde", "Bamidele",
                    "Chidike", "Chike", "Chima", "Chinedu", "Chuma", "Diallo", "Dzigbode", "Ekene", "Fela",
                    "Folami", "Jawara", "Kaikura", "Yero", "Ahmed", "Ashraf", "Baahir", "Babu", "Bahman",
                    "Bassel", "Essam", "Gamal", "Halif", "Idir", "Khalid", "Mahmoud", "Moustafa", "Nabil",
                    "Nakia", "Ramses", "Shakir", "Tariq", "Youssef", "Zuberi", "Abioye", "Addo", "Ade",
                    "Amri", "Darius", "Eze", "Kgosi", "Malik", "Mandlenkosi", "Nkosana", "Oba", "Obayana",
                    "Taj", "Zane", "Alassane", "Amare", "Hasani", "Hasnuu", "Hassan", "Nyillingondo",
                    "Runako", "Ruwa", "Shakil", "Zeen", "Zuri", "Adom", "Barack", "Chinua", "Chinyelu",
                    "Chinyere", "Chukwuemeka", "Eleojo", "Izibekien", "Kirabo", "Lubanzi", "Obasi",
                    "Olufemi", "Omari", "Onkarabile", "Onyinyechi", "Sbusiso", "Simbarashe"
                ],
                "apellidos": [
                    "Mohamed", "Ali", "Ahmed", "Ibrahim", "Mohammed", "Hassan", "Diallo", "Musa", "Abdullahi", 
                    "Abubakar", "Sani", "Traore", "Adamu", "Coulibaly", "Usman", "Umar", "Muhammad", "Osman", 
                    "Muhammed", "Ouedraogo", "John", "Camara", "Abdi", "Adam", "Yusuf", "Moussa", "Ilunga", 
                    "Aliyu", "Mahmoud", "Ngoy", "Garba", "Hussein", "Kone", "Omar", "Tesfaye", "Banda", "Juma", 
                    "Joseph", "Issa", "Bello", "Bah", "Sow", "Ouattara", "Sawadogo", "Deng", "Ismail", "Haruna", 
                    "Solomon", "Barry", "Phiri", "Diarra", "Ndiaye", "Toure", "Idris", "Emmanuel", "Said", 
                    "Getachew", "Keita", "Kasongo", "Abdou", "Cisse", "Saleh", "Yahaya", "Abdalla", "Manuel", 
                    "Peter", "Ba", "Abdallah", "Ahmad", "Samuel", "Tadesse", "Lawal", "Abebe", "Mahamat", 
                    "James", "Girma", "Yakubu", "Salah", "Kamara", "Diop", "Aminu", "Mustafa", "Isah", "Omer", 
                    "Dembele", "Sunday", "Saad", "Eze", "Domingos", "Salisu", "Isa", "Kebede", "Koffi", "Sylla", 
                    "Sidibe", "Bekele", "Suleiman", "Konate", "Akpan", "Francisco", "Hamza", "Kouassi", "António", 
                    "Amadi", "Shehu", "Bala", "Oumarou", "Balde", "Hailu", "Mostafa", "Alemayehu", "Daniel", 
                    "Dlamini", "Aden", "David", "Yao", "Otieno", "Moyo", "Mensah", "Adel", "Salem", "Gamal", 
                    "Taha", "Saidi", "Ndlovu", "Baba", "Banza", "Saeed", "Kouadio", "Umaru", "Amadou", "Adamou", 
                    "Fofana", "Alemu", "Paul", "Gomes", "da Silva", "Jean", "Abbas", "Kouame", "Charles", "Almaz", 
                    "Bashir", "Awad", "Pedro", "Kabore", "Mulu", "Farah", "Mekonnen", "Okafor", "Michael", "Abdo", 
                    "Teshome", "Kamal", "Mwangi", "Kouakou", "Genet", "Abera", "Simon", "Gueye", "Saidu", "Abba", 
                    "Diakite", "Mustapha", "Diouf", "Doumbia", "Ntumba", "dos Santos", "Khalil", "Mulugeta", 
                    "Mussa", "Salih", "Rabiu", "Maiga", "Fall", "Paulo", "Dauda", "Thomas", "Sayed", "Mujinga", 
                    "Sangare", "Yousif", "Moses", "Fernandes", "Sántos", "Langa", "Okeke", "Amin", "Konan", 
                    "Ngalula", "Hamadou", "Sulaiman", "Hamed", "Haile", "Ramadan", "Abakar", "Audu", "Ojo", 
                    "Elias", "Maina", "Rakotomalala", "Samir", "Abdoulaye", "Owusu", "Okoro", "Sesay", "Adebayo", 
                    "Hamid", "Zulu", "Johnson", "Kapinga", "Tilahun", "Mansour", "Ferreira", "Ally", "Sanogo", 
                    "Faye", "Worku", "Tsegaye", "Dube", "Abdu", "Rakotonirina", "Abu", "Alhassan", "Tsehay", 
                    "Okon", "Asefa", "Hussien", "Pereira", "Lopes", "Abdullah", "Koroma", "Nkulu", "Conde", 
                    "Mwamba", "Abebech", "Muhammadu", "Chukwu", "Miguel", "Jemal", "Desta", "Ado", "Kyungu", 
                    "Odhiambo", "Ochieng", "Cossa", "Igwe", "Udo", "Neto", "Ajayi", "Sale", "Seid", "Mesfin", 
                    "Elsayed", "Gabriel", "Assefa", "Ncube", "Ngoma", "Dicko", "Magdy", "Jimoh", "Samson", 
                    "Khaled", "Birhanu", "da Costa", "Ngoie", "Fatuma", "Mamadou", "Khumalo", "Bamba", "Sarr", 
                    "Mendes", "Tembo", "Yeshi", "Sithole", "Obi", "Nkosi", "Abdul", "Meseret", "Kedir", 
                    "Nwachukwu", "Samba", "Akello", "Nour", "Harouna", "N'Guessan", "Martins", "Soro", "Okello", 
                    "George", "Haji", "Sule", "Kabiru", "Chol", "Sibanda", "Bangura", "Mbuyi", "Sisay", 
                    "Mwale", "Hamdy"
                ]
            }
        },
    "Asiatico": {
            "1": {
                "nombres": [
                    "Nushi", "Mohammed", "Muhammad", "Wei", "Mohammad", "Yan", "Li", "Ying", "Abdul", "Ali",
                    "Hui", "Mohamed", "Hong", "Min", "Lei", "Yu", "Xin", "Bin", "Ping", "Lin", "Sri", "Yong",
                    "Ram", "Ming", "Siti", "Ling", "Qing", "Sunita", "Ghulam", "Anita", "Ahmed", "Peng",
                    "Qiang", "Yun", "Ahmad", "Jin", "Noor", "Rong", "Chao", "Santosh", "Anh", "Gang", "Yue",
                    "Fatima", "Kyaw", "Na", "Sanjay", "Zahra", "Sunil", "Nur", "Mei", "Gita", "Jianhua",
                    "Masmaat", "Xiaoyan", "Mo", "Rajesh", "Abdullah", "Liping", "Ramesh", "Manoj", "Bibi",
                    "Ashok", "Ning", "Rekha", "Aung", "Chen", "Hassan", "Mary", "Lan", "Fatemeh", "Zhen",
                    "Suresh", "Kai", "Anil", "Vijay", "Maryam", "Cheng", "Syed", "Lakshmi", "Mina", "Raju",
                    "Xiang", "Long", "Haiyan", "Manju", "Mehmet", "Jianping", "Hai", "Nan", "Vinod", "Rama",
                    "Kun", "Suman", "Lihua", "Zaw", "Shanti", "Zhiqiang", "Saleh", "Xiaohong", "Ibrahim",
                    "Wai", "Kamal", "Rajendra", "Rita", "Linh", "Gul", "Raj", "Rina", "Asha", "Lijun",
                    "Maria", "Dinesh", "Ni", "Elena", "Shan", "Xiaoli", "Meng", "Jianguo", "Usha", "Xiaoping",
                    "Fatma", "Kiran", "Sima", "Rani", "Jianjun", "Ha", "Rakesh", "Krishna", "Sita", "Lijuan",
                    "Tingting", "Zhi", "Ei", "Sergey", "Han", "Tuan", "Thanh", "Zin", "Xiaoling", "Xuan",
                    "Dilip", "Tun", "Yuanyuan", "Mahdi", "Xiaodong", "Zainab", "An", "Amit", "Hung", "Pushpa",
                    "Maya", "Mustafa", "Ajay", "Xiaming", "Mohamad", "Xing", "Mohan", "Laoshi", "Amir", "Hasan",
                    "Di", "Ravi", "Laxmi", "Munni", "Saeed", "Urmila", "Mukesh", "Tatyana", "Kenji", "Radha",
                    "Aleksandr", "Natalya", "Huan", "Jingjing", "Zhiyong", "Chun", "Arun", "Hiroshi", "Savitri",
                    "Salma", "Shankar", "Yanping", "Gopal", "Xiaohua", "Lalita", "Jianming", "Sushila", "Ismail",
                    "Xiaofeng", "Sangita", "Weidong", "Olga", "Agus", "Sumitra", "Ganesh", "Nirmala", "Xiaojun",
                    "Zhiming", "Haji", "Shuang", "Mahesh", "Qiong", "Quan", "Yin", "Trang", "Zhigang", "Hang",
                    "Rahul", "Xiaoying", "Savita", "Phuong", "Abdo", "Asma", "Zhiwei", "Jianfeng", "Xiaohui",
                    "Xiaomei", "Chi", "Hongmei", "Shu", "Xuemei", "Song", "Mira", "Shiv", "Anwar", "Jitendra",
                    "Hussein", "Raja", "Dung", "Prakash", "Saroj", "Chunyan", "Irina", "Jinhua", "Hongwei",
                    "Weiwei", "Dongmei", "Thu", "Tong", "Zhihua", "Naseem", "Surendra", "Jyoti", "Man", "Sarita",
                    "Guoqiang", "Seyyed", "Ayşe", "Mahendra", "Andrey", "O", "Narayan", "Vladimir", "Anna",
                    "Ayesha", "Pramod", "Sultan", "Kavita", "Hongyan", "Pa", "Hari", "Xiaoyu", "Hossein",
                    "Shigeru", "Mamta", "Jianxin", "Guohua", "Abdel", "Myat", "Muhamad", "Nurul", "Lwin",
                    "Jianzhong", "Thao", "Punam", "Nam", "Sai", "Mostafa", "Mahmoud", "Subhash", "Masoumeh",
                    "Zhijun", "Pradip", "Uma", "A", "Ekaterina", "Cong", "Yanling", "Hamid", "Zhihong",
                    "Shanshan", "Than", "Huy", "Svetlana", "Weihua", "Imran", "Ahmet", "Dipak", "Kalpana",
                    "Parvati", "Le", "Abbas", "Farzana", "Yuhua", "Liming", "Wenjun", "Ranjit", "Yanhong",
                    "Kamla", "Lihong", "Junjie", "Qun", "Prem", "Sharmin", "Shah", "Jianmin", "Ka", "Ngoc",
                    "Ran", "Lal", "Xiaolin", "Son", "Shobha", "Nasir", "Sadia", "Tian", "Umesh", "Thuy",
                    "Arif", "Yanhua", "Weimin", "Xiaoqing", "Jianwei", "Ravindra", "Sachiko", "Minh", "Smt",
                    "Phyo", "Yingying", "Pankaj", "Emine", "Durga", "Wenjie", "Ta", "Haibo", "Van", "Ma",
                    "Arjun", "Weiping", "Naresh", "Dmitriy", "Renu", "Nguyen", "Xian", "Shyam", "Reza",
                    "Masako", "Basanti", "Priyanka", "Babu", "Lingling", "Huimin", "Anastasiya", "Nusrat",
                    "Shakuntala", "Aziz", "Qinghua", "Pramila", "Sarah", "Katsumi", "Samina", "Sakina",
                    "Zhihui", "Nasreen", "Lixin", "Chunhua", "Yanyan", "Xiaomin", "John", "Khaled", "Hieu",
                    "Xiaowei", "Alexander", "Weiming", "Hoa", "Hoang", "Yoko", "Amina", "Haiying", "Laksmi",
                    "Shila", "Shahid", "Saraswati", "Halima", "Bharat", "Kamala", "Ganga", "Pei", "Nga",
                    "Mariam", "Nasrin", "Zhenhua", "Wenjing", "Liying", "Khadija", "Marina", "Tien", "Zhijian",
                    "Omar", "Haitao", "Jamila", "Guoliang", "Ca", "Yen", "Tu", "Yasmin", "Zhiping", "Yumei",
                    "Kailash", "Sangeeta", "Yuping", "Xiaoxia", "Satish", "Jianhui", "Huong", "Haifeng",
                    "Samira", "Sheikh", "Mohsen", "Michiko", "Mi", "Guoqing", "Zhimin", "Hatice", "Chandra",
                    "Hlaing", "Sandeep", "Weihong", "Kusum", "Guoping", "Sandhya", "Deepak", "Razia", "Iman",
                    "Archana", "Ai", "Jannatul", "Tara", "Rana"
                ],
                "apellidos": [
                    "Chen", "Cheng", "Cheung", "Chiu", "Dong", "Feng", "Gao", "Huang", "Lam", "Lee", 
                    "Li", "Liu", "Luo", "Ma", "Song", "Sun", "Tsui", "Wang", "Wong", "Wu", 
                    "Xu", "Yang", "Yeung", "Zhang", "Zhao", "Hashimoto", "Hayashi", "Ikeda", "Inoue", "Ito", 
                    "Kato", "Kimura", "Kobayashi", "Matsumoto", "Mori", "Nakajima", "Nakamura", "Saito", "Sasaki", "Sato", 
                    "Shimizu", "Suzuki", "Takahashi", "Tanaka", "Watanabe", "Yamada", "Yamaguchi", "Yamamoto", "Yamazaki", "Yoshida", 
                    "Cho", "Choi", "Han", "Hong", "Hwang", "Iang", "Jang", "Jeon", "Jung", "Kim", 
                    "Ko", "Kwon", "Lim", "Moon", "Oh", "Park", "Ryang", "Seo", "Shin", "Son", 
                    "Yoon", "Bui", "Dang", "Dao", "Do", "Duong", "Ho", "Hoang", "Huynh", "Lam", 
                    "Le", "Ly", "Mai", "Ngo", "Nguyen", "Pham", "Phan", "Phi", "Phung", "To", 
                    "Tran", "Trinh", "Truong", "Vu", "Vyong", "Adulyadej", "Apinya", "Boonmee", "Chaidee", "Chaiya", 
                    "Charoen", "Dangda", "Kasem", "Lamsam", "Makok", "Nantasri", "Narong", "Ngam", "Rattana", "Swangsri", 
                    "Siriporn", "Somboon", "Somchai", "Thana", "Tularak", "Udomsilp", "Ungphakorn", "Wanglee", "Wichai", "Yoovidhya", 
                    "Aquino", "Bautista", "Castillo", "Castro", "Cruz", "De Guzman", "Dela Cruz", "De Leon", "Domingo", "Fernandez", 
                    "Flores", "Francisco", "Garcia", "Gonzales", "Lopez", "Martinez", "Mendoza", "Perez", "Ramos", "Reyes", 
                    "Rivera", "Sanchez", "Santos", "Torres", "Villanueva", "Bai", "Chopra", "Das", "Devi", "Gujarati", 
                    "Gupta", "Kapoor", "Kaur", "Khan", "Khatri", "Kumar", "Kumari", "Lal", "Malik", "Patel", 
                    "Patil", "Ram", "Rao", "Reddy", "Shah", "Sharma", "Shukla", "Singh", "Tamil", "Yadav", 
                    "Zhou", "Vo", "Kang", "Tan", "Setiawan", "Pereira"
                ]
            }
        },
    "Europa": {
            "1": {
                "nombres": [
                    "Alex", "Nikita", "George", "Vlad", "Dima", "Daniel", "Ivan", "Adam", "Sasha", "Max", 
                    "Artem", "Alexander", "Sergey", "Dmitry", "David", "Andrew", "Peter", "Andrey", "Anton", "Martin", 
                    "Igor", "Nick", "Kirill", "Mateusz", "Jakub", "John", "Pavel", "Michael", "Vladimir", "Denis", 
                    "Maxim", "Oleg", "Egor", "Bartek", "Roman", "Szymon", "Dominik", "Kamil", "Ilya", "Mark", 
                    "Jan", "Vadim", "Robert", "Danil", "Kacper", "Patryk", "Vladislav", "Daniil", "Filip", "Adrian", 
                    "Alexey", "Bogdan", "Michal", "Paul", "Kuba", "Marek", "Patrik", "Lukas", "Andrei", "Alexandr", 
                    "Dawid", "Marcin", "Wojtek", "Chris", "Ruslan", "Przemek", "Tomas", "Yaroslav", "Tomek", "Mike", 
                    "Gleb", "Vova", "Kostya", "Balazs", "Dmitriy", "Misha", "Maciej", "Sebastian", "Artur", "Petr", 
                    "Arthur", "Karol", "Stelios", "Zhenya", "Kostas", "Eugene", "Attila", "Richard", "Konstantinos", "Tamas", 
                    "Balint", "Damian", "Boris", "Stas", "Kolya", "Piotr", "Sergei", "Victor", "Roma", "Antek", 
                    "Bence", "Ondra", "Thanos", "Artyom", "Maksim", "Dimitris", "Bartosz", "Mate", "Roland", "Yan", 
                    "Ilia", "Stefan", "Marcel", "Matvey", "Matthew", "Nik", "Slava", "Maciek", "Manos", "Marton", 
                    "Timur", "Vitaliy", "Mikhail", "Christos", "Taras", "Laszlo", "Tom", "Krystian", "Tasos", "Thomas", 
                    "Dan", "Honza", "Nazar", "Oliver", "Luka", "Andreas", "Wojciech", "Karel", "Krisztian", "Arseniy", 
                    "Panagiotis", "Milan", "Krzysztof", "Pasha", "Radek", "Aleksander", "Nicolas", "Grisha", "Wiktor", "Samuel", 
                    "Aris", "Kristof", "Bill", "Aleksey", "Bohdan", "Istvan", "Christopher", "Henry", "Levente", "Jim", 
                    "Matej", "Konstantin", "Yegor", "Danila", "Hubert", "Dorin", "Simon", "Gabor", "Marios", "Pawel", 
                    "Danya", "Bulat", "Apostolis", "Marko", "Valera", "Alexandros", "Zoltan", "Fedor", "Leo", "Giorgos", 
                    "Andy", "Szabolcs", "Ali", "Stepan", "Dennis", "Norbert", "Emil", "Greg", "Giannis", "Den", 
                    "Sam", "Joseph", "Viktor", "Alan", "Zsolt", "Luke", "Grzegorz", "Gregory", "Tomasz", "Angelos", 
                    "Edward", "Jacek", "Aleksei", "Nikola", "Pantelis", "Maks", "Zsombor", "Mikolaj", "Janek", "Steven", 
                    "Vojta", "Marius", "Tibor", "Evgeny", "Marian", "Benjamin", "Patrick", "Darek", "Emmanuel", "Serhiy", 
                    "Ales", "Alexandru", "Evangelos", "Mansur", "Gosha", "Tim", "Anatoly", "Botond", "Vitaly", "Haris", 
                    "Arek", "Mihail", "Zahar", "Denys", "Ognyan", "Rafit", "Andras", "Rostislav", "Mario", "Art", 
                    "Christian", "Jirka", "Aggelos", "Antonis", "Yury", "Lefteris", "Manolis", "Erik", "Maxime", "Alexandre", 
                    "Quentin", "Kevin", "Julien", "Antoine", "Clement", "Romain", "Florian", "Hugo", "Valentin", "Guillaume", 
                    "Theo", "Anthony", "Alexis", "Jeremy", "Louis", "Adrien", "Dylan", "Mathieu", "Vincent", "Nathan", 
                    "Baptiste", "Axel", "Jordan", "Enzo", "James", "Corentin", "Jack", "Jonathan", "Gabriel", "Raphael", 
                    "Remi", "Thibault", "Robin", "Ben", "Loic", "William", "Matthieu", "Sebastien", "Aurelien", "Marco", 
                    "Matteo", "Arnaud", "Damien", "Mathis", "Luca", "Tristan", "Bastien", "Andrea", "Dorian", "Maxence", 
                    "Ryan", "Jules", "Marc", "Francois", "Yanis", "Thibaut", "Charles", "Florent", "Mickael", "Liam", 
                    "Francesco", "Yann", "Erwan", "Cyril", "Benoit", "Cedric", "Mohamed", "Fabien", "Gaetan", "Morgan", 
                    "Jerome", "Jean", "Tony", "Ethan", "Olivier", "Lorenzo", "Jason", "Charlie", "Mehdi", "Lewis", 
                    "Alessandro", "Xavier", "Remy", "Joe", "Pablo", "Oscar", "Ruben", "Harry", "Antonio", "Josh", 
                    "Tanguy", "Alejandro", "Killian", "Mael", "Elias", "Patrick", "Miguel", "Noah", "Sylvain", "Felix", 
                    "Laurent", "Joshua", "Antonin", "Jake", "Dimitri", "Aymeric", "Callum", "Manuel", "Evan", "Sean", 
                    "Matt", "Mathias", "Ludovic", "Bryan", "Aaron", "Stephane", "Jamie", "Matthias", "Noe", "Eric", 
                    "Sergio", "Davide", "Gregory", "Federico", "Jimmy", "Sofiane", "Leon", "Jonas", "Philippe", "Fabio", 
                    "Javier", "Christophe", "Allan", "Yoann", "Gregoire", "Carlos", "Frederic", "Johan", "Connor", "Mateo", 
                    "Jacob", "Giovanni", "Franck", "Kieran", "Bruno", "Rayan", "Joel", "Jose", "Justin", "Geoffrey", 
                    "Stefano", "Diego", "Etienne", "Gael", "Nico", "Juan", "Pedro", "Lilian", "Alberto", "Kylian", 
                    "Titouan", "Simone", "Alvaro", "Luis", "Yannick", "Giuseppe", "Yohan", "Esteban", "Riccardo", "Brandon", 
                    "Logan", "Gauthier", "Luc", "Cameron", "Matheo", "Brian", "Brice", "Gabriele", "Daniele", "Jorge", 
                    "Will", "Emilien", "Scott", "Edouard", "Sami", "Joris", "Isaac", "Eliott", "Fabian", "Flavien", 
                    "Kyle", "Stephen", "Nassim", "Yacine", "Nils", "Yohann", "Loris", "Samy", "Karl", "Ugo", 
                    "Alessio", "Timothee", "Tobias", "Pierrick", "Steve", "Tommy", "Amine", "Frank", "Fred", "Jessy", 
                    "Pascal", "Jay", "Mattia", "Elliot", "Camille", "Gabin", "Amaury", "Charly", "Owen", "Teddy", 
                    "Emanuele", "Marvin", "Raul", "Roberto", "Augustin", "Cristian", "Ahmed", "Alban", "Ismael", "Danny", 
                    "Marcus", "Mikael", "Yassine", "Albert", "Karim", "Filippo", "Ayoub", "Reece", "Melvin", "Manu", 
                    "Michele", "Ronan", "Elie", "Gautier", "Leonardo", "Philipp", "Hakim", "Armand", "Thibaud", "Loick", 
                    "Timothe", "Francisco", "Dani", "Rudy", "Emile", "Jesus", "Alfie", "Conor", "Nathanael", "Alain", 
                    "Mathys", "Rafael", "Colin", "Angel", "Gaspard", "Marcos", "Lucien", "Nolan", "Andre", "Joao", 
                    "Tyler", "Fernando", "Lenny", "Youssef", "Rene", "Hamza", "Giacomo", "Anis", "Thierry", "Omar", 
                    "Abdel", "Johannes", "Donovan", "Younes", "Rodolphe", "Joachim", "Joey", "Jesse", "Edoardo", "Lionel", 
                    "Rhys", "Bilal", "Eliot", "Philip", "Ludo", "Florentin", "Fran", "Joan", "Malo", "Maximilien", 
                    "Markus", "Kai", "Dario", "Gwendal", "Toni", "Ricardo", "Nicola", "Stan", "Andres", "Ewen", 
                    "Bradley", "Jim", "Eddy", "Ulysse"
                ],
                "apellidos": [
                    "Garcia", "Martin", "Muller", "Rodriguez", "Fernandez", "Gonzalez", "Lopez", "Martinez", 
                    "Sanchez", "Perez", "Ivanov", "Schmidt", "Smith", "Jones", "Gomez", "Schneider", 
                    "Fischer", "Petrov", "Meyer", "Weber", "Thomas", "Ruiz", "Williams", "Jimenez", 
                    "Hernandez", "Rossi", "Magomedov", "Wagner", "Brown", "Diaz", "Kuznetsov", "Smirnov", 
                    "Moreno", "Taylor", "Silva", "Hansen", "Popov", "Nowak", "Simon", "Santos", 
                    "Toth", "Becker", "Hoffmann", "Alvarez", "Shevchenko", "Davies", "Nagy", "Costa", 
                    "Jensen", "Munoz", "Schulz", "Bauer", "Klein", "Koch", "Pereira", "Wilson", 
                    "Johansson", "Andersson", "Ferreira", "Nielsen", "Richter", "Evans", "Bondarenko", 
                    "Romero", "Russo", "Wolf", "Varga", "Kovalenko", "Schafer", "Szabo", "Johnson", 
                    "Marin", "Pavlov", "Kovacs", "Alonso", "Novikov", "Ramos", "Ferrari", "Schmid", 
                    "Kravchenko", "Torres", "Sokolov", "Meier", "Navarro", "Roberts", "Gutierrez", 
                    "Zimmermann", "Braun", "Huber", "Vasilev", "Miller", "Karlsson", "Schmitt", 
                    "Schwarz", "Walker", "Volkov", "Neumann", "Berger", "Peters", "Andreev", "Romanov", 
                    "Andersen", "Popa", "Schroder", "Bernard", "Gil", "Tkachenko", "Pedersen", "Thompson", 
                    "Robinson", "White", "Wright", "Mayer", "Hughes", "Lange", "Fernandes", "Rodrigues", 
                    "Hofmann", "Michel", "Nilsson", "Martins", "David", "Kowalski", "Hartmann", "Aliev", 
                    "Lehmann", "Morozov", "Makarov", "Jovanovic", "Green", "Horvath", "Murphy", "Patel", 
                    "Castro", "Hall", "Lang", "Clarke", "Kelly", "Edwards", "Werner", "Oliveira", 
                    "Dominguez", "Maier", "Keller", "Esposito", "Yilmaz", "Kiss", "Schmitz", "Lewis", 
                    "Pinto", "Jansen", "Krause", "Walter", "Kozlov", "Harris", "Kruger", "Jackson", 
                    "Fuchs", "Dubois", "Moore", "Vazquez", "Hill", "Zaytsev", "Wood", "Larsen", 
                    "Serrano", "Lebedev", "Sergeeva", "Stepanov", "Richard", "Kaiser", "Turner", 
                    "Clark", "Ramirez", "Bianchi", "Scott", "Eriksson", "Lopes", "Lee", "Zakharov", 
                    "Nikolaev", "Petrovic", "Sousa", "King", "Ward", "Melnyk", "Nikolic", "Ali", 
                    "Herrmann", "Robert", "Gomes", "Lambert", "Cooper", "Mikhaylov", "Colombo", 
                    "Morris", "Popescu", "Schulze", "Molina", "Vidal", "Frolov", "Konig", "Beck", 
                    "Blanco", "Singh", "Khan", "Orlov", "Morgan", "Delgado", "Petersen", "Durand", 
                    "Moreau", "Roth", "Ribeiro", "Anderson", "Mazur", "Larsson", "Romano", "Jung", 
                    "Ortega", "Kovalchuk", "Egorov", "Ahmed", "Morales", "Kotov", "Watson", "Winkler", 
                    "Pop", "Kohler", "James", "Adam", "Suarez", "Laurent", "Frank", "Allen", 
                    "Kaya", "Marques", "Harrison", "Alves", "Baker", "Yakovlev", "Cruz", "Young", 
                    "Campbell", "Bell", "Medvedev", "Borisov", "Savchenko", "Vogel", "Baumann", 
                    "Roman", "Winter", "Moller", "Radu", "Mitchell", "Marchenko", "Almeida", "Leroy", 
                    "Carvalho", "Belov", "Lucas", "Ortiz", "Mironov", "Goncalves", "Sergeev", 
                    "Lewandowski", "Phillips", "Collins", "Christensen", "Nikitin", "Scholz", 
                    "Rubio", "Molnar", "Hahn", "Arnold", "Georgiev", "Olsson", "Murray", "Berg", 
                    "Persson", "Dimitrov", "Kowalczyk", "Demir", "Aleksandrov", "Koval", "Parker", 
                    "Paul", "Weiss", "Adams", "Svensson", "Graf", "Moroz", "Boiko", "Friedrich", 
                    "Dias", "Olsen", "Bennett", "Schubert", "Walsh", "Bruno", "Bondar", "Franco", 
                    "Gallo", "Rudenko", "Serra", "Kaminski", "Semenov", "Lysenko", "Antonov", 
                    "Ilic", "Sanz", "Stewart", "Lorenz", "Petrenko", "Teixeira", "Henry", "Price", 
                    "Shaw", "Zielinski", "Campos", "Richardson", "Medina", "Simpson", "Rose", 
                    "Szymanski", "Haas", "Steiner", "Rusu", "Ricci", "Cook", "Griffiths", "Albrecht", 
                    "Carter", "Cox", "Garrido", "Marshall", "Gray", "Bailey", "Schuster", "Gunther", 
                    "Sommer", "Kraus", "Dupont", "Iglesias", "Cortes", "Ozturk", "Castillo", 
                    "Nguyen", "Shevchuk", "Dumitru", "de Jong", "Morel", "Sorensen", "Brandt", 
                    "Rasmussen", "da Silva", "Mendes", "Roux", "Ryan", "Vincent", "Schumacher", 
                    "Correia", "Gruber", "Franke", "Isaev", "Nemeth", "Greco", "Bohm", "Djordjevic", 
                    "Stevens", "Vogt", "Marino", "Hussain", "Rey", "Jacobs", "Ciobanu", "Nunez", 
                    "Li", "Ludwig", "Fournier", "Markovic", "Jankowski", "Sala", "Kramer", "Pavlenko", 
                    "Stan", "Girard", "Giordano", "Graham", "Moser", "Cano", "Nicolas", "Rosa", 
                    "Akhmedov", "Lozano", "Urban", "Richards", "Stein", "Johansen", "Conti", 
                    "Lefebvre", "Guerrero", "Blanc", "Rizzo", "Duarte", "Sahin", "Kozlowski", 
                    "Guerra", "Pavlovic", "Jager", "Byrne", "Jordan", "Ellis", "Moreira", "Farkas", 
                    "Sidorov", "Matei", "Leon", "Bertrand", "Mason", "Celik", "Engel", "Villa", 
                    "Baran", "Gheorghe", "Flores", "Otto", "Mercier", "Aydin", "Calvo", "Karpenko"
                ]
            }
        }
}

def asignar_familia_cultural(pais_nom, cont):

    if pais_nom == "Brasil": return "Brasil"

    if cont == "Sudamérica" or pais_nom == "España" or cont == "Norteamérica": return "Hispano"

    if cont == "África": return "Africano"

    if cont == "Asia": return "Asiatico"

    if cont == "Europa": return "Europa"

    return "Anglo"


# Se asume que DATA_IDENTIDAD y CONFIG_POSICIONES están definidos arriba

def generar_poblacion_mundial(jugadores_por_equipo=22):
    conn = sqlite3.connect("futbol_manager.db")
    cursor = conn.cursor()

    # IDs de países europeos (Pesos: ID baja = Probabilidad alta)
    ids_europeos = [
        11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 43, 71, 73, 74, 
        75, 76, 77, 78, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 91, 92, 93, 
        94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 
        109, 110, 111, 112
    ]
    max_id = max(ids_europeos)
    min_id = min(ids_europeos)
    pesos_europeos = [(max_id + min_id - id_val) for id_val in ids_europeos]

    # Obtenemos los equipos
    cursor.execute("""
        SELECT e.id, e.nombre, p.nombre, p.continente, p.id, e.presupuesto 
        FROM equipos e
        JOIN paises p ON e.pais_id = p.id
    """)
    equipos = cursor.fetchall()

    # Limpiamos datos previos para evitar conflictos de FK
    cursor.execute("DELETE FROM atributos")
    cursor.execute("DELETE FROM jugadores")
    
    print(f"Generando jugadores para {len(equipos)} equipos...")

    for eq_id, eq_nombre, pais_nom, cont, pais_id_local, presupuesto in equipos:
        familia_local = asignar_familia_cultural(pais_nom, cont)
        
        # Calidad base según presupuesto (Escala 1-200)
        # Equipos TOP (City, Madrid) ~150-160 CA. Equipos bajos ~70-80 CA.
        calidad_base_eq = min(max(int(presupuesto / 30), 65), 165)

        for i in range(jugadores_por_equipo):
            # 1. Nacionalidad (70% Local, 30% Extranjero top)
            if random.random() < 0.7:
                nac_id = pais_id_local
                familia = familia_local
            else:
                nac_id = random.choices(ids_europeos, weights=pesos_europeos, k=1)[0]
                familia = "Europa" if nac_id != 13 else "Anglo"

            # 2. Nombre
            try:
                sub_key = random.choice(list(DATA_IDENTIDAD[familia].keys()))
                pool = DATA_IDENTIDAD[familia][sub_key]
                nombre_completo = f"{random.choice(pool['nombres'])} {random.choice(pool['apellidos'])}"
            except:
                nombre_completo = f"Jugador {random.randint(100, 999)}"

            # 3. Posición
            if i < 2: pos = "Portero"
            elif i < 9: pos = "Defensa"
            elif i < 16: pos = "Mediocentro"
            else: pos = "Delantero"

            # 4. CA, PA y Edad
            ca = calidad_base_eq + random.randint(-15, 20)
            pa = ca + random.randint(5, 35)
            ca, pa = min(ca, 200), min(pa, 200)
            edad = random.randint(17, 34)

            # --- INSERCIÓN EN TABLA JUGADORES ---
            cursor.execute("""
                INSERT INTO jugadores (equipo_id, nacionalidad_id, nombre, posicion, ca, pa, edad) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (eq_id, nac_id, nombre_completo, pos, ca, pa, edad))
            
            jugador_id = cursor.lastrowid

            # --- GENERACIÓN Y ASIGNACIÓN DE ATRIBUTOS (1-20) ---
            # El multiplicador asegura que un CA alto resulte en atributos altos
            multiplicador = ca / 200 
            stats = {}
            config = CONFIG_POSICIONES[pos]

            for attr in TODOS_LOS_ATRIBUTOS:
                if attr in config["clave"]:
                    # Rango 14-20 para cracks, ajustado por multiplicador
                    val = int(14 * multiplicador) + random.randint(3, 6)
                elif attr in config["secundarios"]:
                    # Rango 10-16
                    val = int(10 * multiplicador) + random.randint(2, 5)
                else:
                    # Rango 5-12
                    val = int(5 * multiplicador) + random.randint(1, 4)
                
                stats[attr] = min(max(val, 1), 20)

            # --- INSERCIÓN EN TABLA ATRIBUTOS ---
            cursor.execute("""
                INSERT INTO atributos (
                    jugador_id, remate, pase, regate, entrada, control, vision, 
                    posicionamiento, anticipacion, determinacion, velocidad, 
                    resistencia, fuerza, reflejos, agilidad
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                jugador_id, stats["Remate"], stats["Pase"], stats["Regate"], 
                stats["Entrada"], stats["Control"], stats["Visión"], 
                stats["Posicionamiento"], stats["Anticipación"], stats["Determinación"], 
                stats["Velocidad"], stats["Resistencia"], stats["Fuerza"], 
                stats["Reflejos"], stats["Agilidad"]
            ))

    conn.commit()
    conn.close()
    print(f"✅ Población completada. {len(equipos) * jugadores_por_equipo} jugadores y sus atributos creados.")

if __name__ == "__main__":
    generar_poblacion_mundial()