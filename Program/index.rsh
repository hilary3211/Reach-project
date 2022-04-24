'reach 0.1';
const [isHand, ROCK, PAPER, SCISSORS] = makeEnum(3)

const [isOutcome, B_WINS, DRAW, A_WINS] = makeEnum(3)

const winner = (handA, handB) => ((handA + (4 - handB)) % 3)



assert(winner(ROCK, PAPER) == B_WINS)
assert(winner(PAPER, ROCK) == A_WINS)
assert(winner(ROCK, ROCK) == DRAW)

forall(UInt, handA =>
    forall(UInt, handB =>
        assert(isOutcome(winner(handA, handB)))))

forall(UInt, (hand) =>
    assert(winner(hand, hand) == DRAW))


const Player = {
    ...hasRandom,
    getHand: Fun([], UInt),
    getHand1: Fun([], UInt),
    getHand2: Fun([], UInt),
    seeOutcome: Fun([UInt], Null),
    informTimeout: Fun([], Null)
};

export const main = Reach.App(() => {
    const Alice = Participant('Alice', {
        ...Player,
        wager: UInt,
        deadline: UInt
    });
    const Bob = Participant('Bob', {
        ...Player,
        acceptWager: Fun([UInt], Null),
    });

    init();


    Alice.only(() => {
        const wager = declassify(interact.wager)
    })

    Alice.publish(wager)
        .pay(wager)
    commit()


    Bob.only(() => {
        interact.acceptWager(wager)
    })
    Bob.pay(wager)
    commit()
    Alice.only(() => {
        const _handAlice = interact.getHand()
        const [_commitAlice, _saltAlice] = makeCommitment(interact, _handAlice)
        const commitAlice = declassify(_commitAlice)
    })
    Alice.publish(commitAlice)
    commit()

    unknowable(Bob, Alice(_handAlice, _saltAlice))

    Bob.only(() => {
        const handBob = declassify(interact.getHand())
    })
    Bob.publish(handBob)
    commit()

    Alice.only(() => {
        const saltAlice = declassify(_saltAlice)
        const handAlice = declassify(_handAlice)
    })

    Alice.publish(saltAlice, handAlice)

    checkCommitment(commitAlice, saltAlice, handAlice)
    const outcome = winner(handAlice, handBob)

    each([Alice, Bob], () => {
        interact.seeOutcome(outcome)
    })
    commit()

    Alice.only(() => {
        const _handAlice2 = interact.getHand1()
        const [_commitAlice2, _saltAlice2] = makeCommitment(interact, _handAlice2)
        const commitAlice2 = declassify(_commitAlice2)
    })
    Alice.publish(commitAlice2)
    commit()

    unknowable(Bob, Alice(_handAlice2, _saltAlice2))

    Bob.only(() => {
        const handBob2 = declassify(interact.getHand1())
    })
    Bob.publish(handBob2)
    commit()

    Alice.only(() => {
        const saltAlice2 = declassify(_saltAlice2)
        const handAlice2 = declassify(_handAlice2)
    })

    Alice.publish(saltAlice2, handAlice2)

    checkCommitment(commitAlice2, saltAlice2, handAlice2)


    const outcome2 = winner(handAlice2, handBob2)

    each([Alice, Bob], () => {
        interact.seeOutcome(outcome2)
    })
    commit()





    Alice.only(() => {
        const _handAlice3 = interact.getHand2()
        const [_commitAlice3, _saltAlice3] = makeCommitment(interact, _handAlice3)
        const commitAlice3 = declassify(_commitAlice3)
    })
    Alice.publish(commitAlice3)
    commit()

    unknowable(Bob, Alice(_handAlice3, _saltAlice3))

    Bob.only(() => {
        const handBob3 = declassify(interact.getHand2())
    })
    Bob.publish(handBob3)
    commit()

    Alice.only(() => {
        const saltAlice3 = declassify(_saltAlice3)
        const handAlice3 = declassify(_handAlice3)
    })

    Alice.publish(saltAlice3, handAlice3)

    checkCommitment(commitAlice3, saltAlice3, handAlice3)


    const outcome3 = winner(handAlice3, handBob3)




    const [forAlice, forBob] =
        outcome2 == A_WINS && outcome == A_WINS || outcome == A_WINS && outcome3 == A_WINS || outcome2 == A_WINS && outcome3 == A_WINS ? [2, 0] :
            outcome2 == B_WINS && outcome == B_WINS || outcome == B_WINS && outcome3 == B_WINS || outcome2 == B_WINS && outcome3 == B_WINS ? [0, 2] :
                [1, 1] /* tie */

    transfer(forAlice * wager).to(Alice)
    transfer(forBob * wager).to(Bob)
    commit();

    each([Alice, Bob], () => {
        interact.seeOutcome(outcome3)
    })
})