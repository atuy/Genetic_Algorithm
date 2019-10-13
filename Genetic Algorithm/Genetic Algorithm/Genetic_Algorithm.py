
import random
import string

input_pw = input("비밀번호를 입력하시오 : ")
min_len = 2
max_len = 15

#랜덤으로 단어를 생성하는 함수
def generate_word(length):
    #tmp = "~!@#$%^&*()_+|][}{-=?><,./`"
    result = ''
    x = ''.join(random.sample(string.ascii_letters + string.digits, k=length))
    return x

def generate_population(size, min_len, max_len):
    #유전 알고리즘의 최초의 아이들 즉 비밀번호의 조합
    population = []
    for i in range(size):
        length = i % (max_len - min_len + 1) + min_len
        population.append(generate_word(length))
    return population


#생성된 아이들의 성능 측정
def fitness(password, test_word):
    score = 0

    #길이가 다를경우
    if len(password) != len(test_word):
        return score
    
    # 만약 길이가 맞으면 0.5점 점수 증가
    len_score = 0.5
    score += len_score

    #문자 위치 비교
    for i in range(len(password)):
        if password[i] == test_word[i]:
            score += 1

    #백점 만점에 몇점?
    return score / (len(password) + len_score) * 100


#성능이 좋은 아이들을 선발
def compute_performace(population, password):
    performance_list = []
    for individual in population:
        score = fitness(password, individual)
        
        #일단 길이는 맞은경우
        if score > 0:
            pred_len = len(individual)
        performance_list.append([individual, score])

    #점수가 높은 순서로 정렬
    population_sorted = sorted(performance_list, key=lambda x: x[1], reverse=True)
    return population_sorted, pred_len

#살아남은 아이들을 정할 함수
def select_survivors(population_sorted, best_sample, lucky_few, password_len):
    next_generation = []

    #성능이 좋은 아이를 살린다
    for i in range(best_sample):
        if population_sorted[i][1] > 0:
            next_generation.append(population_sorted[i][0])

    #운이 좋은 아이를 살린다
    lucky_survivors = random.sample(population_sorted, k=lucky_few)
    for l in lucky_survivors:
        next_generation.append(l[0])
    
    #만약 세대의 아이들이 적을 경우 랜덤으로 생성
    while len(next_generation) < best_sample + lucky_few:
        next_generation.append(generate_word(length=password_len))

    # 셔플
    random.shuffle(next_generation)
    return next_generation

#다음 세대 생성을 위한 교배
def create_child(individual1, individual2):
    child = ''
    #길이가 다를 경우를 대비해 적은 길이를 가진 것을 반환
    min_len_ind = min(len(individual1), len(individual2))
    for i in range(min_len_ind):
        #50%의 확률로 부모의 성능을 가짐
        if (int(100 * random.random()) < 50):
            child += individual1[i]
        else:
            child += individual2[i]
    return child

# 다음 세대 생성
def create_children(parents, n_child):
    next_population = []
    #부모의 갯수 / 2 
    for i in range(int(len(parents)/2)):
        for j in range(n_child):
            next_population.append(create_child(parents[i], parents[len(parents) - 1 - i]))
    return next_population



 #돌연변이 생성
def mutate_word(word):
    #랜덤으로 인덱스를 뽑는다
    idx = int(random.random() * len(word))
    if (idx == 0):
        word = random.choice(string.ascii_letters + string.digits) + word[1:]
    else:
        word = word[:idx] + random.choice(string.ascii_letters + string.digits) + word[idx+1:]
    #랜덤한 인덱스의 자리를 랜덤한걸로 집어넣어 돌연변이를 만들어 준다
    return word


#이번 세대의 아이들을 돌연변이 화 시킴
def mutate_population(population, chance_of_mutation):
    for i in range(len(population)):
        if random.random() * 100 < chance_of_mutation:
            population[i] = mutate_word(population[i])
    return population


n_generation = 100000
population = 100
best_sample = 20
lucky_few = 20
n_child = 5
chance_of_mutation = 10

pop = generate_population(size=population, min_len=min_len, max_len=max_len)

for g in range(n_generation):
    pop_sorted, pred_len = compute_performace(population=pop, password=input_pw)
    pop_avg = 0
    pop_sum = 0
    for i in range(len(pop_sorted)):
        pop_sum += pop_sorted[i][1]
    pop_avg = pop_sum / len(pop_sorted)           
    if int(pop_sorted[0][1]) >= 100:
        print('===== %s번째 비밀번호 탐색 =====' % (g + 1))
        print(pop_sorted[0], pop_avg, sep="   ")
        print('\n비밀번호를 찾았습니다!! :  %s' % (pop_sorted[0][0]))
        break
    
    survivors = select_survivors(population_sorted=pop_sorted, best_sample=best_sample, lucky_few=lucky_few, password_len=pred_len)
    
    children = create_children(parents=survivors, n_child=n_child)

    new_generation = mutate_population(population=children, chance_of_mutation=10)
    
    pop = new_generation
    #if g % 10 ==0:
    #    print(pop)
    print('===== %s번째 비밀번호 탐색 =====' % (g + 1))
    print(pop_sorted[0] , pop_avg, sep="   ")
    #print(random.choice(pop_sorted))