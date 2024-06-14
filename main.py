from audio_convert import extract_text_from_pdf, chapters_generator
from audio_convert import chunk_converter, combine_chunks

if __name__ == "__main__":
    pdf_path = "/Users/sohierelsafty/Downloads/48-laws-of-power/The-48-Laws-of-Power-Robert-Greene.pdf"  # Path to your PDF file
    txt_path = "/Users/sohierelsafty/Downloads/48-laws-of-power/The-48-Laws-of-Power.txt"  # Path for the output text file
    output_dir = "/Users/sohierelsafty/Downloads/48-laws-of-power"
    from_page = 15
    to_page = 782

    content_list = [
    ('Introduction', 'PREFACE'),
    ('Ch1', 'LAW 1 NEVER OUTSHINE THE MASTER'),
    ('Ch2', 'LAW 2 NEVER PUT TOO MUCH TRUST IN FRIENDS, LEARN HOW TO USE ENEMIES'),
    ('Ch3', 'LAW 3 CONCEAL YOUR INTENTIONS'),
    ('Ch4', 'LAW 4 ALWAYS SAY LESS THAN NECESSARY'),
    ('Ch5', 'LAW 5 SO MUCH DEPENDS ON REPUTATION—GUARD IT WITH YOUR LIFE'),
    ('Ch6', 'LAW 6 COURT ATTENTION AT ALL COST'),
    ('Ch7', 'LAW 7 GET OTHERS TO DO THE WORK FOR YOU, BUT ALWAYS TAKE THE CREDIT'),
    ('Ch8', 'LAW 8 MAKE OTHER PEOPLE COME TO YOU—USE BAIT IF NECESSARY'),
    ('Ch9', 'LAW 9 WIN THROUGH YOUR ACTIONS, NEVER THROUGH ARGUMENT'),
    ('Ch10', 'LAW 10 INFECTION: AVOID THE UNHAPPY AND UNLUCKY'),
    ('Ch11', 'LAW 11 LEARN TO KEEP PEOPLE DEPENDENT ON YOU'),
    ('Ch12', 'LAW 12 USE SELECTIVE HONESTY AND GENEROSITY TO DISARM YOUR VICTIM'),
    ('Ch13', 'LAW 13 WHEN ASKING FOR HELP, APPEAL TO PEOPLE’S SELFINTEREST, NEVER TO THEIR ...'),
    ('Ch14', 'LAW 14 POSE AS A FRIEND, WORK AS A SPY'),
    ('Ch15', 'LAW 15 CRUSH YOUR ENEMY TOTALLY'),
    ('Ch16', 'LAW 16 USE ABSENCE TO INCREASE RESPECT AND HONOR'),
    ('Ch17', 'LAW 17 KEEP OTHERS IN SUSPENDED TERROR: CULTIVATE AN AIR OF UNPREDICTABILITY'),
    ('Ch18', 'LAW 18 DO NOT BUILD FORTRESSES TO PROTECT YOURSELF—ISOLATION IS DANGEROUS'),
    ('Ch19', 'LAW 19 KNOW WHO YOU’RE DEALING WITH—DO NOT OFFEND THE WRONG PERSON'),
    ('Ch20', 'LAW 20 DO NOT COMMIT TO ANYONE'),
    ('Ch21', 'LAW 21 PLAY A SUCKER TO CATCH A SUCKER—SEEM DUMBER THAN YOUR MARK'),
    ('Ch22', 'LAW 22 USE THE SURRENDER TACTIC: TRANSFORM WEAKNESS INTO POWER'),
    ('Ch23', 'LAW 23 CONCENTRATE YOUR FORCES'),
    ('Ch24', 'LAW 24 PLAY THE PERFECT COURTIER'),
    ('Ch25', 'LAW 25 RE-CREATE YOURSELF'),
    ('Ch26', 'LAW 26 KEEP YOUR HANDS CLEAN'),
    ('Ch27', 'LAW 27 PLAY ON PEOPLE’S NEED TO BELIEVE TO CREATE A CULTLIKE FOLLOWING'),
    ('Ch28', 'LAW 28 ENTER ACTION WITH BOLDNESS'),
    ('Ch29', 'LAW 29 PLAN ALL THE WAY TO THE END'),
    ('Ch30', 'LAW 30 MAKE YOUR ACCOMPLISHMENTS SEEM EFFORTLESS'),
    ('Ch31', 'LAW 31 CONTROL THE OPTIONS: GET OTHERS TO PLAY WITH THE CARDS YOU DEAL'),
    ('Ch32', 'LAW 32 PLAY TO PEOPLE’S FANTASIES'),
    ('Ch33', 'LAW 33 DISCOVER EACH MAN’S THUMBSCREW'),
    ('Ch34', 'LAW 34 BE ROYAL IN YOUR OWN FASHION: ACT LIKE A KING TO BE TREATED LIKE ONE'),
    ('Ch35', 'LAW 35 MASTER THE ART OF TIMING'),
    ('Ch36', 'LAW 36 DISDAIN THINGS YOU CANNOT HAVE: IGNORING THEM IS THE BEST REVENGE'),
    ('Ch37', 'LAW 37 CREATE COMPELLING SPECTACLES'),
    ('Ch38', 'LAW 38 THINK AS YOU LIKE BUT BEHAVE LIKE OTHERS'),
    ('Ch39', 'LAW 39 STIR UP WATERS TO CATCH FISH'),
    ('Ch40', 'LAW 40 DESPISE THE FREE LUNCH'),
    ('Ch41', 'LAW 41 AVOID STEPPING INTO A GREAT MAN’S SHOES'),
    ('Ch42', 'LAW 42 STRIKE THE SHEPHERD AND THE SHEEP WILL SCATTER'),
    ('Ch43', 'LAW 43 WORK ON THE HEARTS AND MINDS OF OTHERS'),
    ('Ch44', 'LAW 44 DISARM AND INFURIATE WITH THE MIRROR EFFECT'),
    ('Ch45', 'LAW 45 PREACH THE NEED FOR CHANGE, BUT NEVER REFORM TOO MUCH AT ONCE'),
    ('Ch46', 'LAW 46 NEVER APPEAR TOO PERFECT'),
    ('Ch47', 'LAW 47 DO NOT GO PAST THE MARK YOU AIMED FOR; IN VICTORY, LEARN WHEN TO STOP'),
    ('Ch48', 'LAW 48 ASSUME FORMLESSNESS'),
    ]

    extract_text_from_pdf(pdf_path, txt_path, from_page, to_page)

    # Extract chapters based on the content list
    chapters_generator(txt_path, content_list, output_dir)

    textfile_path = "/Users/sohierelsafty/Downloads/48-laws-of-power/ch1"
    speaker_voice = "Djano.mp3"
    audio_output_dir = "/Users/sohierelsafty/Downloads/48-laws-of-power/audio"
    prefix = "ch1"  # Example prefix for chapter 1
    chunk_converter(textfile_path, speaker_voice, audio_output_dir, prefix)
    combine_chunks(audio_output_dir, prefix, f"{prefix}_combined.wav")


#Later
#TODO: Combine the converted chapters into one audio file with limit of 4 hours


#TODO: automate what we were doing on capcut, adding the audio on a standard cover
#TODO: automate the file uploading on youtube
#TODO: create an interface for the whole project to make it easier to use
#TODO: asign an audio voice depend on the gender of the writer to mimic the feeling