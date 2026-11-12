from drafter import *
from dataclasses import dataclass, field
from bakery import assert_equal


set_website_title("Environmental Impact Simulator")
set_site_information(
    author="Madelynn Conard",
    description="See how normal human actions effect the environment.",
    sources="Thanks to the Drafter docs.",
    planning=["plan.pdf", "design.pdf"],
    links=[]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class Outcome:
    title: str
    description: str
    impact_score: int


@dataclass
class State:
    current_page: str
    selected_action: str
    outcomes: list[Outcome]
    status_message: str
    total_impact: int
    outcomes_viewed: int
    reflection: str


"""
Below are helper functions to help the program function
"""

def add_outcome(state: State,title: str,description: str, score: int) -> None:
    """
    Adds a new environmental outcome.
    """
    state.outcomes.append(
        Outcome(title, description, score)
    )

    state.total_impact += score
    state.outcomes_viewed += 1


def outcome_summary(state: State) -> str:
    """
    Creates a string containing all outcomes. Demonstrates the required loop.
    """

    result = ""

    for outcome in state.outcomes:
        result += (
            outcome.title +
            ": " +
            outcome.description +
            " Score: " +
            str(outcome.impact_score) +
            "\n"
        )

    return result


@route
def index(state: State) -> Page:
    """
    This is the "home page" of the website. It is what you see when you first open
    the server, and displays the three "negative" actions.
    """
    return Page(state, [

        "Environmental Impact Simulator!",

        "\nChoose a negative action:",

        TextBox(
            "action",
            state.selected_action
        ),

        "\nType one of:",
        "\nBuild Homes",
        "\nDrive Car",
        "\nSingle-Use Plastics\n",

        Button(
            "Submit Negative Action",
            negative_router
        ),

        Button(
            "Positive Actions",
            positive_actions
        )
    ])




@route
def negative_router(state: State,
                    action: str) -> Page:
    """
    Directs user based on chosen "negative" action.
    """

    state.selected_action = action


    if action == "Build Homes":
        return build_homes(state)

    elif action == "Drive Car":
        return drive_car(state)

    elif action == "Single-Use Plastics":
        return single_use_plastic(state)

    state.status_message = (
        "Please enter a valid action."
    )

    return index(state)

@route
def build_homes(state: State) -> Page:
    """
    If a user clicks "build homes", they are directed to this page where the negative effect of building
    homes is displayed.
    """
    state.current_page = "build_homes"
    add_outcome(
        state,
        "Habitat Loss",
        "Building homes can remove animal habitats.",
        -15
    )

    state.status_message = (
        "Forests may be cleared for development. Also meaning animal habitats are destroyed."
    )

    return Page(state, [
        "Building Homes:",

        state.status_message,

        Button(
            "Return Home",
            index
        )
    ])



@route
def drive_car(state: State) -> Page:

    """
    If a user clicks "drive car", they are directed to this page where the negative effect of driving cars
    is displayed.
    """
    state.current_page = "drive_car"

    add_outcome(
        state,
        "Air Pollution",
        "Cars release greenhouse gases.",
        -20
    )

    state.status_message = (
        "Driving produces carbon emissions, which add to the trapped gases in the atmosphere."
    )

    return Page(state, [
        "Driving Cars:",

        state.status_message,

        Button(
            "Return Home",
            index
        )
    ])

    state.status_message = (
        "Driving produces carbon emissions."
    )

    return Page(state, [
        "Driving Cars",

        state.status_message,

        Button(
            "Return Home",
            index
        )
    ])




@route
def single_use_plastic(state: State) -> Page:
    """
    If a user clicks "single use plastic", they are directed to this page where the negative effect of
    using single use plastics is displayed.
    """
    state.current_page = "single_use_plastic"

 

    if state.selected_action == (
        "Single-Use Plastics"
    ):

        add_outcome(
            state,
            "Ocean Pollution",
            "Plastic frequently reaches oceans.",
            -25
        )

        state.status_message = (
            "Plastic harms marine life."
        )

    return Page(state, [
        "Single-Use Plastics:",

        state.status_message,

        Button(
            "Return Home",
            index
        )
    ])


@route
def positive_actions(state: State) -> Page:
    """
    When a user clicks through all the negative actions, they can click the button "positive actions"
    which brings you to the positive actions page to click through three more "positive" actions.
    """
    return Page(state, [

        "Positive Actions",

        TextBox(
            "positive_action",
            ""
        ),

        "\nType one of:",
        "\nPrevent Deforestation",
        "\nUse Reusables",
        "\nBike or Walk\n",

        Button(
            "Submit Positive Action",
            positive_router
        ),

        Button(
            "Results",
            end_page
        )
    ])


@route
def positive_router(state: State, positive_action: str) -> Page:
    """
    Directs user based on chosen "positive" action.
    """
    
    if positive_action == (
        "Prevent Deforestation"
    ):
        return prevent_deforestation(state)

    elif positive_action == (
        "Use Reusables"
    ):
        return reusables(state)

    elif positive_action == (
        "Bike or Walk"
    ):
        return biking_or_walking(state)

    return positive_actions(state)


@route
def prevent_deforestation(state: State) -> Page:
    """
    If a user clicks "prevent deforestation", they are directed to this page where the positive effect of
    preventing deforestation is displayed. 
    """
    add_outcome(
        state,
        "Protected Forests",
        "Trees absorb carbon dioxide.",
        20
    )

    return Page(state, [
        "Prevent Deforestation:",

        "Protecting forests improves ecosystems.",

        Button(
            "Return",
            positive_actions
        )
    ])


@route
def reusables(state: State) -> Page:
    """
    If a user clicks "reusable", they are directed to this page where the positive effect of
    using reusables is displayed. 
    """
    add_outcome(
        state,
        "Reduced Waste",
        "Reusable items reduce landfill waste.",
        15
    )

    return Page(state, [
        "Use Reusables:",

        "Reusable products reduce pollution.",

        Button(
            "Return",
            positive_actions
        )
    ])


@route
def biking_or_walking(state: State) -> Page:
    """
    If a user clicks "biking or walking", they are directed to this page where the positive effect of
    using biking or walking is displayed. 
    """
    add_outcome(
        state,
        "Reduced Emissions",
        "Walking creates no emissions.",
        25
    )

    return Page(state, [
        "Bike or Walk:",

        "Alternative transportation helps Earth.",

        Button(
            "Return",
            positive_actions
        )
    ])


@route
def end_page(state: State) -> Page:

    """
    This is the "end page" of the website. It is what you see when you go through all the actions
    or don't, and displays the results, the total impact score, the outcomes, the reflection text
    box, and the play again button.
    """

    if state.outcomes_viewed >= 3:

        state.status_message = (
            "You explored enough actions!"
        )

    else:

        state.status_message = (
            "Explore more actions first."
        )

    return Page(state, [

        "Results:",

        state.status_message,

        "\nTotal Impact Score: "
        + str(state.total_impact),

        "\nOutcomes:\n",

        outcome_summary(state),

        "\nReflection:",

        TextBox(
            "reflection",
            state.reflection
        ),

        Button(
            "Play Again",
            reset_game
        )
    ])

@route
def reset_game(state: State) -> Page:
    """
    This function returns you back to the home page to restart the whole game.
    """
    state.current_page = "home"
    state.selected_action = ""
    state.outcomes = []
    state.status_message = ""
    state.total_impact = 0
    state.outcomes_viewed = 0
    state.reflection = ""

    return index(state)

#unit tests

# ----------------------------------------
# add_outcome
# ----------------------------------------

test_state = State("home", "", [], "", 0, 0, "")

add_outcome(
    test_state,
    "Test Outcome",
    "Test Description",
    10
)

assert_equal(len(test_state.outcomes), 1)
assert_equal(test_state.total_impact, 10)
assert_equal(test_state.outcomes_viewed, 1)


# ----------------------------------------
# outcome_summary
# ----------------------------------------

test_state = State("home", "", [], "", 0, 0, "")

add_outcome(
    test_state,
    "Pollution",
    "Bad for environment",
    -5
)

assert_equal(
    outcome_summary(test_state),
    "Pollution: Bad for environment Score: -5\n"
)


# ----------------------------------------
# index
# ----------------------------------------

test_state = State("home", "", [], "", 0, 0, "")

index(test_state)

assert_equal(test_state.current_page, "home")


# ----------------------------------------
# negative_router
# ----------------------------------------

test_state = State("home", "", [], "", 0, 0, "")

negative_router(
    test_state,
    "Build Homes"
)

assert_equal(
    test_state.selected_action,
    "Build Homes"
)


# ----------------------------------------
# build_homes
# ----------------------------------------

test_state = State("home", "", [], "", 0, 0, "")

build_homes(test_state)

assert_equal(
    test_state.current_page,
    "build_homes"
)

assert_equal(
    len(test_state.outcomes),
    1
)


# ----------------------------------------
# drive_car
# ----------------------------------------

test_state = State("home", "", [], "", 0, 0, "")

drive_car(test_state)

assert_equal(
    test_state.current_page,
    "drive_car"
)

assert_equal(
    len(test_state.outcomes),
    1
)


# ----------------------------------------
# single_use_plastic
# ----------------------------------------

test_state = State(
    "home",
    "Single-Use Plastics",
    [],
    "",
    0,
    0,
    ""
)

single_use_plastic(test_state)

assert_equal(
    test_state.current_page,
    "single_use_plastic"
)

assert_equal(
    len(test_state.outcomes),
    1
)


# ----------------------------------------
# positive_actions
# ----------------------------------------

test_state = State("home", "", [], "", 0, 0, "")

positive_actions(test_state)

assert_equal(
    test_state.current_page,
    "home"
)


# ----------------------------------------
# positive_router
# ----------------------------------------

test_state = State("home", "", [], "", 0, 0, "")

positive_router(
    test_state,
    "Use Reusables"
)

assert_equal(
    len(test_state.outcomes),
    1
)


# ----------------------------------------
# prevent_deforestation
# ----------------------------------------

test_state = State("home", "", [], "", 0, 0, "")

prevent_deforestation(test_state)

assert_equal(
    len(test_state.outcomes),
    1
)

assert_equal(
    test_state.total_impact,
    20
)


# ----------------------------------------
# reusables
# ----------------------------------------

test_state = State("home", "", [], "", 0, 0, "")

reusables(test_state)

assert_equal(
    len(test_state.outcomes),
    1
)

assert_equal(
    test_state.total_impact,
    15
)


# ----------------------------------------
# biking_or_walking
# ----------------------------------------

test_state = State("home", "", [], "", 0, 0, "")

biking_or_walking(test_state)

assert_equal(
    len(test_state.outcomes),
    1
)

assert_equal(
    test_state.total_impact,
    25
)


# ----------------------------------------
# end_page
# ----------------------------------------

test_state = State(
    "home",
    "",
    [],
    "",
    0,
    3,
    ""
)

end_page(test_state)

assert_equal(
    test_state.status_message,
    "You explored enough actions!"
)


# ----------------------------------------
# reset_game
# ----------------------------------------

test_state = State(
    "build_homes",
    "Build Homes",
    [
        Outcome(
            "Test",
            "Test",
            -10
        )
    ],
    "message",
    -10,
    5,
    "reflection"
)

reset_game(test_state)

assert_equal(
    test_state.selected_action,
    ""
)

assert_equal(
    len(test_state.outcomes),
    0
)

assert_equal(
    test_state.total_impact,
    0
)

assert_equal(
    test_state.outcomes_viewed,
    0
)

assert_equal(
    test_state.reflection,
    ""
)


start_server(
    State("home", "", [],
        "",
        0,
        0,
        ""
    )
)
