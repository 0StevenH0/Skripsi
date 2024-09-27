import re
from collections import defaultdict


class KnowledgeHandler:
    __slots__ = ["text","level_patterns"]

    def __init__(self):
        self.text = None
        self.level_patterns = {
            "level_7": r"\[7\[(.*?)\]\]",
            "level_6": r"\[6\[(.*?)\]\]",
            "level_5": r"\[5\[(.*?)\]\]",
            "level_4": r"\[4\[(.*?)\]\]",
            "level_3": r"\[3\[(.*?)\]\]",
            "level_2": r"\[2\[(.*?)\]\]",
            "level_1": r"\[1\[(.*?)\]\]",
            "level_0": r"\[\[(.*?)\]\]"
        }

    def temporary_knowledge(self):

        text = {
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[ACCOUNTING]] [2[(@BEKASI)]] [[DESKRIPSI PROGRAM]]": "Accounting Technology Program, merupakan Program Sarjana Akuntansi, School of Accounting, Binus University yang berlokasi di Kampus Binus Bekasi. Program Sarjana Akuntansi ini menekankan pada kurikulum Akuntansi yang diintegrasikan pada penguasaan penerapan teknologi akuntansi (accounting software) bagi mahasiswanya.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[ACCOUNTING]] [2[(@BEKASI)]] [[PROSPEK KARIR]]": "Professional Accountant (yang fokus pada bidang, tetapi tidak terbatas sebagai) : Business Transformer, Data Navigator dan Digital Playmaker. Lulusan dapat juga berkarir sebagai Public Accountant, Management Accountant, Internal Auditor, Government Accountant, Government Auditor, Tax Consultant, Banker, Finance  Analyst, Entrepreneur",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[ACCOUNTING]] [2[(@BEKASI)]] [[[ACCREDITATION]]": "Unggul | HEEACT",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[ACCOUNTING]] [2[(@BEKASI)]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[ACCOUNTING]] [2[(@BEKASI)]] [[ACADEMIC TITLES]]": "Ak.",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[TAXATION]] [[PROGRAM DESCRIPTION]]": "Program Taxation dirancang agar calon mahasiswa memiliki kompetensi Akuntansi, khususnya Perpajakan, kemampuan untuk berpikir analitis dan problem solving, serta keterampilan menggunakan teknologi sehingga kamu mampu menganalisis serta merancang strategi perpajakan yang komprehensif dengan memanfaatkan aplikasi perpajakan.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[TAXATION]] [[PROSPECTIVE CAREER]]": "Konsultan Pajak (Tax Consultant), Ahli Pajak Perusahaan (Tax Corporate Analist), Pengacara Pajak (Tax Attorney), Ahli Transfer Pricing (Transfer Pricing Specialist), Ahli Bea Cukai-Expor- Impor (Export Import Tax Specialist), Perencana Teknologi Perpajakan (Digital Tax Planner/Taxologist), Perencana Wajib Pajak Miliuner (HNWI Tax planner), Perencana Pajak Dalam Negeri & Internasional (Domestic & International Tax planner)",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[TAXATION]] [[ACCREDITATION]]": "Unggul | HEEACT",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[TAXATION]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[TAXATION]] [[ACADEMIC TITLE]]": "S.Ak.",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[FINANCE]] [[PROGRAM DESCRIPTION]]": "Dengan bergabung di Program Finance, kamu akan belajar state of the art dunia keuangan saat ini: pasar modal, lembaga keuangan: bank dan non-bank serta Digital Finance. Kamu akan mempelajari keahlian yang diperlukan sebagai seorang praktisi keuangan yang handal seperti analisa laporan keuangan, valuasi dan simulasi investasi, data analytics serta aplikasi teknologi inovatif. Disamping itu kamu juga berkesempatan untuk memperoleh sertifikasi internasional bergengsi: Certified Financial Analyst (CFA).Pembelajaran akan dilakukan dengan pendekatan teori dan praktik yang diampu oleh para dosen pengajar dan praktisi berpengalaman. Sebagai mahasiswa program Finance, kamu juga akan memiliki akses ke database yang biasa digunakan oleh professional keuangan global yakni Bloomberg dan Osiris",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[FINANCE]] [[PROSPECTIVE CAREER]]": "Financial Analyst, Treasurer, Financial Controller, Business and Development Analyst, Investment Advisor, Risk Analyst, Portfolio and Fund Manager, Trader, Credit Analyst",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[FINANCE]] [[ACCREDITATION]]": "Unggul | HEEACT",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[FINANCE]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[FINANCE]] [[ACADEMIC TITLE]]": "S.Ak.",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[ACCOUNTING]] [[PROGRAM DESCRIPTION]]": "Program Accounting BINUS UNIVERSITY dirancang untuk memudahkan kamu mempelajari hal hal yang berkaitan dengan laporan keuangan, kebijakan keuangan, laporan kinerja perusahaan, pemeriksaan laporan keuangan, laporan pertanggungjawaban kepada stakeholder, pengambilan keputusan bisnis, serta pengelolaan dan analitik data keuangan ( Accounting Data Analytics) termasuk juga penerapan prinsip akuntansi dan profesi akuntan. Dengan mempelajari program ini kamu bisa berkarir sebagai akuntan, auditor, management accountant, business analyst, data navigator, fraud investigator, tax accountant maupun tax officer.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[ACCOUNTING]] [[PROSPECTIVE CAREER]]": "Management Accountant, Auditor (External Auditor, Internal Auditor, Forensic Auditor, and Information System Auditor), Financial Controller and Analyst, Financial Planner, Business & System Analyst, Tax Accountant, External Business Advisor, Accounting Data Analyst, and Software Specialist.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[ACCOUNTING]] [[ACCREDITATION]]": "Unggul | HEEACT",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[ACCOUNTING]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF ACCOUNTING]] [3[ACCOUNTING]] [[ACADEMIC TITLE]]": "S.Ak.",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[FASHION]] [[PROGRAM DESCRIPTION]]": "Fashion program BINUS UNIVERSITY telah berdiri sejak 2010 berawal dari hasil kolaborasi antara BINUS UNIVERSITY INTERNATIONAL dan Northumbria University, Newcastle, Inggris. Lalu per tahun ajaran 2024/2025 Fashion program hadir di BINUS @Alam Sutera dengan cita-cita dan semangat yang sama yaitu untuk menjadi sekolah Fashion terbaik di Indonesia, Fashion program terus mengupayakan menghasilkan tenaga profesional terampil yang mampu memecahkan masalah di bidang nya. Untuk mendukung kegiatan belajar mengajar yang efektif, BINUS UNIVERSITY menyediakan fasilitas studio yang sangat baik, termasuk ruang kerja produksi garmen, ruang eksperimen tekstil (batik, tenun, sablon dan rajut), laboratorium komputer, dan studio fotografi. Fashion Program menyediakan rencana studi personal yang fleksibel berdasarkan kebutuhan mahasiswa, didukung melalui program perkuliahan (2+1+1) dimana dalam 2,5 tahun kuliah mahasiswa di siapkan menggapai karier dan peluang Dual Degree (S.Ds. & BA with Hons.). Selain itu mahasiswa dapat memilih peminatan Fashion Design atau Fashion Retail Management, yang memberikan kesempatan untuk mendalami praktik fashion dan bekerja dalam industri fashion sesungguhnya. Fashion Program Binus University juga mengutamakan pengalaman praktis, proyek kolaboratif dengan profesional, dan mempersiapkan mahasiswa untuk mengembangkan keterampilan dan mempersiapkan karier mereka.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[FASHION]] [[PROSPECTIVE CAREER]]": "Berbagai peluang karir di industri Fashion akan diperkenalkan dan mahasiswa akan dipersiapkan selama masa studi. Kurikulum terintegrasi dirancang dan dikembangkan untuk mendukung mahasiswa dalam membangun keterampilan teknis dan non-teknis serta terlibat dengan industry. Salah satu program dalam pengembangan karir yaitu program magang untuk setiap mahasiswa di mana mahasiswa dapat melakukan proyek nyata sebagai studi praktis dalam konteks industri. Program ini mengembangkan kemampuan siswa untuk terlibat dalam praktik profesional, dan tanggung jawab etika dan organisasi. Selain itu, serangkaian studi/kunjungan lapangan ke para profesional dan industri akan dilakukan untuk memberikan dasar yang baik untuk memiliki gambaran yang luas tentang industri. Pengalaman-pengalaman ini mendukung aspirasi karir individu dan dapat memberikan jaringan sosial dan profesional. Lulusan program Fashion diharapkan siap sebagai desainer untuk produksi dan manufaktur menengah hingga massal, sebagai tanggapan terhadap berbagai tingkat pasar. Lulusan Fashion program BINUS UNIVERSITY dapat berkarir dalam bidang berikut tanpa terkecuali :",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[FASHION]] [[ACCREDITATION]]": "A | HEEACT",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[FASHION]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[FASHION]] [[ACADEMIC TITLE]]": "S.Ds. & BA (Hons) (Optional)",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [2[(@SEMARANG)]] [[PROGRAM DESCRIPTION]]": "Program Studi Desain Komunikasi Visual menyiapkan generasi muda menjadi komponen pembangunan bangsa, memiliki ilmu pengetahuan lokal dan global dari komunikasi visual yang kreatif dengan mengusung sejarah dan nilai-nilai lokal, teknologi, dan kewirausahaan sehingga mampu berkarya dan diterima oleh industri kreatif, masyarakat, dan bangsa Indonesia melalui penerapan ilmu desain komunikasi visual dengan memanfaatkan teknologi komunikasi dan informasi.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [2[(@SEMARANG)]] [[PROSPECTIVE CAREER]]": "Graphic Designer, Brand Designer, Art Director, Inhouse Designer, Interaction designer, AR/VR visual developer, Video mapping Designer, Immerse Designer, Exhibition Designer, Content Creator, Creative writer, Creative storyteller, Social media Specialist, Digital photographer, Motion graphic designer",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [2[(@SEMARANG)]] [[ACCREDITATION]]": "Baik I HEEACT",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [2[(@SEMARANG)]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [2[(@SEMARANG)]] [[ACADEMIC TITLE]]": "S.Ds.",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [2[(@MALANG)]] [[PROGRAM DESCRIPTION]]": "Manusia tidak akan pernah lepas dari kebutuhan akan ruang interior untuk beraktifitas dan tempat perlindungan. Dengan banyaknya prospek karir dari keilmuan ini, program studi ini menyiapkan kamu untuk menjadi seorang desainer interior handal yang tidak hanya kreatif dalam mengolah ruang, namun juga memiliki pemahaman desain yang benar, adaptif terhadap perkembangan teknologi di bidang interior, serta berwawasan lingkungan tanpa melupakan akar budaya lokal kita yang begitu kaya dan unik.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [2[(@MALANG)]] [[PROSPECTIVE CAREER]]": "Interior Design Consultant, Interior Design Contractor, Furniture Designer, Home Accessories Designer, Lighting Designer, Exhibition Designer, Visual Merchandiser, Manufacturer of Interior Accessories",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [2[(@MALANG)]] [[ACCREDITATION]]": "Baik",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [2[(@MALANG)]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [2[(@MALANG)]] [[ACADEMIC TITLE]]": "S.Ds.",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [2[(@MALANG)]] [[SCHOLARSHIP]]": "Learn more about BINUS Scholarship",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [2[(@BANDUNG)]] [[LABEL : BANNER PROGRAM AKADEMIK INTERIOR DESIGN BANDUNG]]": "[[PROGRAM DESCRIPTION]] Interior Design (Bandung) is a multidiscipline major which specializes in interior consultants and construction creative businesses that intend to increase diversity due to change market factors and professional practices. Furthermore, we enhance our students to respond to the boundaries in a way to extend the purposeful innovative, and creative industries of Interior Design. Interior Design (Bandung) BINUS University is supported by lecturers with industry experience. Our students will experience real-world project flow as they advanced through their courses in this major, such as planning, research, and designing processes. Our students will learn how to apply technology, culture, business, and environmental aspects in their designs. In Interior Design (Bandung) department, students will be encouraged to implement several aspects as the way to solve problems regarding to the construction and aesthetical elements in Interior design. Students are prepared to excel in preparing interior concept design, planning, presenting a professional visualization for their interior projects for residential, retail, office, hotel, and other public spaces. Techno-design curriculum in our program allows students to comprehend the usage of technology in the learning process. Students will gain basic and advance Computer-Aided knowledge to accommodate challenges to compete as a professional interior designer in the future. Interior design (Bandung)’s graduates of BINUS University will become future interior designer professionally. They are well equipped to work in global firm or becoming a creative entrepreneur. They will be able to compete with other professionals in the industry.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [2[(@BANDUNG)]] [[PROSPECTIVE CAREER]]": "Commercial and Hospitality Design, Furniture and Interior Design Accessories, Techno Interior Design and Smart Living & Environmental Design",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [2[(@BANDUNG)]] [[ACCREDITATION]]": "Baik",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [2[(@BANDUNG)]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [2[(@BANDUNG)]] [[ACADEMIC TITLE]]": "S.Ds.",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [2[(@BANDUNG)]] [[PROGRAM DESCRIPTION]]": "The Visual Communication Design Study Program prepares the young generation to become components of national development, possessing local and global knowledge in visual communication by carrying local history, values, technology, and entrepreneurship. It also prepares them to work and be accepted by the creative industry and society through applying visual communication design by utilizing information and communication technology.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [2[(@BANDUNG)]] [[PROSPECTIVE CAREER]]": "Art Director Graphic Designer Illustrator Photographer Videographer Motion Graphic Designer Digital Imaging Artist Entrepreneur Visual Artist 2D+ Post-production Artist 2D+ Key frame Animator 2D+ Storyboard Artist 2D+ Game Asset Artist 2D+",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [2[(@BANDUNG)]] [[ACCREDITATION]]": "Baik | HEEACT",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [2[(@BANDUNG)]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [2[(@BANDUNG)]] [[ACADEMIC TITLE]]": "S.Ds.",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [2[(@MALANG)]] [[PROGRAM DESCRIPTION]]": "Students are provided with unique capabilities of information technology that can support their future career aspirations in Visual Communication Design by having proficiency in skill & knowledge in synergizing the print, digital, and interactive media. Students can apply their capabilities in a variety of visual communication cases; UX design, brand & branding, information design, design for the public, photography, illustration, typography, and web design into interactive new media design.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [2[(@MALANG)]] [[PROSPECTIVE CAREER]]": "UX Designer Brand Designer Visual Storyteller in Publishing Design Surface Packaging Designer Game Design Visualizer Visual Identity Designer Graphic Designer Illustrator Photographer In-house Designer Government & NGO Institutions Media & News Broadcast Studio Corporate & Retail Industry",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [2[(@MALANG)]] [[ACCREDITATION]]": "Baik I HEEACT",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [2[(@MALANG)]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [2[(@MALANG)]] [[ACADEMIC TITLE]]": "S.Ds.",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [[PROGRAM DESCRIPTION]]": "Program studi Desain Interior adalah tempat bagi para calon praktisi dan pemikir desain. Melalui jurusan ini para lulusan akan dipersiapkan untuk menjadi profesional di bidang desain dengan kompetensi yang kuat dalam memahami potensi mengadaptasi kearifan lokal, memahami dan menggunakan teknologi terkini serta menjadi desainer yang bertanggung jawab dalam nilai-nilai desain berkelanjutan dalam memecahkan berbagai permasalahan. Program ini menawarkan kombinasi teori dan praktik studio, siswa akan memperkaya pengetahuan desain mereka dengan kelas-kelas studio yang berkaitan dengan konstruksi, interior, dan furniture, studi desain dan budaya, komputer untuk desain, pemanfaatan dan pengetahuan material, dan tren desain. Mahasiswa juga dibekali kemampuan berpikir kreatif dalam membangun bisnis melalui mata kuliah Entrepreneurship dan dibekali wawasan yang berkaitan erat dengan Commercial and Hospitality design untuk dapat siap menentukan peran di dunia industri.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [[PROSPECTIVE CAREER]]": "Desainer Interior, Pemilik Konsultan Interior, Kontraktor Interior, Visual Merchandiser, Interior Decorator and Stylist, Penulis Majalah atau Buku, Interior, Lighting Designer, Exhibition Designer, Event Organizer, Facility and Building Management Officer, Buyer dan Retailer untuk perusahaan Furniture",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [[ACCREDITATION]]": "A",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[INTERIOR DESIGN]] [[ACADEMIC TITLE]]": "S.Ds",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [1[NEW MEDIA]] [[PROGRAM DESCRIPTION]]": "Pergeseran peradaban dunia menuju digitalisasi telah mengubah cara kita berinteraksi dengan informasi visual yang tidak hanya terbatas dalam format media; mulai dari perangkat digital, media cetak hingga medium hybrid-interaktif digital & cetak. Kurikulum sudah dirancang untuk dapat bersinergi dengan program enrichment (2+1) +1 hingga proyek tugas akhir.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [1[NEW MEDIA]] [[PROSPECTIVE CAREER]]": "UX Designer, Brand Designer, Visual Storyteller in Publishing Design, Surface Packaging, Designer, Game UI Designer,, Visual Identity Designer, Graphic, Designer, Illustrator, Motion Graphic, Designer, Creative Visualizer, In-, house Designer, Government & NGO Institutions, Media & News, Broadcast Studio, Corporate & Retail Industry",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [1[NEW MEDIA]] [[ACCREDITATION]]": "Unggul | AUN-QA | HEEACT",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [1[NEW MEDIA]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [1[NEW MEDIA]] [[ACADEMIC TITLE]]": "S.Ds",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [1[CREATIVE ADVERTISING]] [[PROGRAM DESCRIPTION]]": "Tertarik pada desain, ilustrasi, video, motion graphic, photography, atau digital imaging? Talenta ini sangat demanding di dunia kreatifitas iklan masa kini! Kalian akan diajarkan konsep kreatif untuk mengolah ide menjadi kampanye komersial yang sangat menarik.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [1[CREATIVE ADVERTISING]] [[PROSPECTIVE CAREER]]": "Art Director, Creative Designer, Social Media Creative & Copywriter, Commercial, Photographer & Videographer",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [1[CREATIVE ADVERTISING]] [[ACCREDITATION]]": "Unggul | AUN-QA | HEEACT",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [1[CREATIVE ADVERTISING]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [1[CREATIVE ADVERTISING]] [[ACADEMIC TITLE]]": "S.Ds",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[FILM]] [[PROGRAM DESCRIPTION]]": "Jurusan Perfilman di Indonesia termasuk salah satu program yang diminati dalam bidang kreatif di era digital saat ini dan BINUS UNIVERSITY termasuk salah satu universitas yang menyelenggarakannya. Dengan akreditasi A dari BAN-PT, Program Studi Film BINUS menggabungkan penggunaan teknologi terbaru dengan pengetahuan serta estika dalam standar tinggi untuk menjawab permintaan tersebut agar menjadi Program Studi yang mampu bersaing secara global khususnya di Asia Tenggara. Mahasiswa tidak hanya belajar teknis memproduksi Film, mereka juga akan dibekali dengan kemampuan dalam pengembangan karakter agar mampu berpikir kritis baik di dalam maupun luar kampus. Salah satunya dengan mengikuti pembelajaran menarik seperti memproduksi Film pendek, pembangunan set Film, menganalisa dan mengkritisi Film. Selain itu, mahasiswa juga akan dilibatkan secara aktif dalam kegiataan organisasi, jurusan serta masyarakat.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[FILM]] [[PROSPECTIVE CAREER]]": "Produser Film, Sutradara Film, Penulis Naskah, Kritikus Film, Akademisi Film, Digital Content, Creator, Jurnalis Film, Film Publicist",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[FILM]] [[ACCREDITATION]]": "A",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[FILM]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[FILM]] [[ACADEMIC TITLE]]": "S.Sn.",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [1[ANIMATION]] [[PROGRAM DESCRIPTION]]": "Belajar animasi di S1 bukan hanya mengasah skill set (penguasaan teknis & tools animasi) saja, tetapi juga mengasah dan menguatkan mindset (penguasaan sosial, budaya, media digital, psikologis, practical research, storytelling dan banyak lagi) terhadap dunia animasi itu sendiri agar dapat menciptakan originalitas berkarya dalam beranimasi.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [1[ANIMATION]] [[PROSPECTIVE CAREER]]": "Animation Entrepreneur (Content Creator) maupun Profesional ,employee (3D/2D artist, Animator, Produser, VFX artist, Concept Art,Motion Grapher, Technical artist, dll)",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [1[ANIMATION]] [[ACCREDITATION]]": "Unggul | AUN-QA | HEEACT",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [1[ANIMATION]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[SCHOOL OF DESIGN]] [3[VISUAL COMMUNICATION DESIGN]] [1[ANIMATION]] [[ACADEMIC TITLE]]": "S.Ds",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[BINUS BUSINESS SCHOOL]] [3[INTERNATIONAL BUSINESS MANAGEMENT]] [1[GLOBAL CLASS]] [[PROGRAM DESCRIPTION]]": "International Business Management (IBM) adalah program sarjana yang dimiliki oleh BINUS UNIVERSITY. Program ini berdurasi selama empat tahun dan bertujuan untuk memberikan pemahaman komprehensif kepada para mahasiswa mengenai operasi bisnis internasional, termasuk ekonomi global, keuangan internasional, manajemen lintas budaya, dan perdagangan internasional. Program IBM dirancang untuk melengkapi para mahasiswa dengan keterampilan dan pengetahuan yang diperlukan agar berhasil dalam lingkungan bisnis global.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[BINUS BUSINESS SCHOOL]] [3[INTERNATIONAL BUSINESS MANAGEMENT]] [1[GLOBAL CLASS]] [[PROSPECTIVE CAREER]]": "International Finance Controller, Import/ Export Compliance Specialist Business Analyst/ Development, International Economist/Banking/Marketing Manager, Multinational Manager, Business Development Manager, International Trade and Customs Manager, International Foreign Policy Advisor, Global Entrepreneur",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[BINUS BUSINESS SCHOOL]] [3[INTERNATIONAL BUSINESS MANAGEMENT]] [1[GLOBAL CLASS]] [[ACCREDITATION]]": "Unggul | AACSB",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[BINUS BUSINESS SCHOOL]] [3[INTERNATIONAL BUSINESS MANAGEMENT]] [1[GLOBAL CLASS]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[BINUS BUSINESS SCHOOL]] [3[INTERNATIONAL BUSINESS MANAGEMENT]] [1[GLOBAL CLASS]] [[ACADEMIC TITLE]]": "S.E.",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[BINUS BUSINESS SCHOOL]] [3[DIGITAL BUSINESS]] [[PROGRAM DESCRIPTION]]": "Program Studi Bisnis Digital akan menyiapkan mahasiswa dalam pengembangan dan pengelolaan bisnis berbasis teknologi digital dan didukung kemampuan financial technology (fintech). Program ini berfokus untuk menciptakan lulusan yang siap membangun usaha rintisan berbasis digital (digital entrepreneur) dan lulusan yang dapat bekerja di perusahaan Nasional maupun Multinasional.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[BINUS BUSINESS SCHOOL]] [3[DIGITAL BUSINESS]] [[PROSPECTIVE CAREER]]": "Digital Entrepreneur (Startup Founder/Co-Founder, Chief Executive Officer & Business Development Manager), Consultant (Digital Business Consultant, Digital Transformation Consultant & Management Consultant), Analyst (Business Analyst, Data Analyst & Digital Business Analyst), Researcher (Digital Business Research, Digital Market Research & Digital Transformation Research), Fintech Specialist (Fintech Developer & Fintech Designer)",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[BINUS BUSINESS SCHOOL]] [3[DIGITAL BUSINESS]] [[ACCREDITATION]]": "Baik",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[BINUS BUSINESS SCHOOL]] [3[DIGITAL BUSINESS]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[BINUS BUSINESS SCHOOL]] [3[DIGITAL BUSINESS]] [[ACADEMIC TITLE]]": "S. Bns.",

            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[BINUS BUSINESS SCHOOL]] [3[ENTREPRENEURSHIP]] [2[(@MALANG)]] [1[BUSINESS CREATION]] [[PROGRAM DESCRIPTION]]": "At Malang Campus, BINUS Business School Undergraduate Program offers an Entrepreneurship Business Creation Study Program. The Program received AACSB international accreditation in 2020. Aligned with this international accreditation, the Program’s curriculum is designed to provide a high-quality teaching and learning experience in supporting the students to become creative and innovative entrepreneurs by developing a structured blueprint for turning ideas into viable ventures or initiatives. The education style also aims to shape the characteristics and the mindset of the student as the future entrepreneur. They have high motivation, dare to try and be innovative in starting a new business in various fields, industries, or markets. Entrepreneurship Business Creation Study Program acquaints entrepreneurship as an academic discipline. The curriculum is designed in particular to prepare students to be creative and innovative entrepreneurs by providing a blueprint for turning ideas into a viable venture or initiative. Entrepreneurship education also aims to shape the characteristics and mindset of entrepreneurs who have high motivation, dare to try and be innovative, which can be applied in various fields of one’s life and career. The Entrepreneurship Business Creation Study Program curriculum is uniquely designed to prepare students to be able to apply their entrepreneurial knowledge and to start new businesses.",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[BINUS BUSINESS SCHOOL]] [3[ENTREPRENEURSHIP]] [2[(@MALANG)]] [1[BUSINESS CREATION]] [[PROSPECTIVE CAREER]]": "Entrepreneur, Intrapreneur, Global entrepreneur, Business Developer, Business Planner, Business Consultant",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[BINUS BUSINESS SCHOOL]] [3[ENTREPRENEURSHIP]] [2[(@MALANG)]] [1[BUSINESS CREATION]] [[ACCREDITATION]]": "Baik I AACSB",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[BINUS BUSINESS SCHOOL]] [3[ENTREPRENEURSHIP]] [2[(@MALANG)]] [1[BUSINESS CREATION]] [[DURATION]]": "4 Tahun",
            "[6[PROGRAM AKADEMIK]] [5[DISIPLIN S1]] [4[BINUS BUSINESS SCHOOL]] [3[ENTREPRENEURSHIP]] [2[(@MALANG)]] [1[BUSINESS CREATION]] [[ACADEMIC TITLE]]": "S.Bns."
        }

        return text

    def question_mapping(self):
        text = {
            "Fasilitas unik apa saja yang tersedia dalam program Fashion di BINUS University yang mendukung mahasiswa dalam studi mereka?" : "[6[DESKRIPSI]] unik apa saja yang tersedia dalam [6[FASHION]] di BINUS University yang mendukung mahasiswa dalam studi mereka?",
            "Bisakah Anda menjelaskan struktur program (2+1+1) pada jurusan Fashion di BINUS University dan bagaimana manfaatnya bagi karier mahasiswa?" : "Bisakah Anda menjelaskan struktur (2+1+1) pada jurusan [3[FASHION]] di BINUS University dan bagaimana manfaatnya bagi [[PROSPECTIVE CAREER]] mahasiswa?",
            "Kompetensi inti apa saja yang ditekankan dalam program Desain Interior di BINUS University untuk memastikan lulusan siap kerja di industri?" : "Kompetensi inti apa saja yang ditekankan dalam [6[INTERIOR DESIGN]] di BINUS University untuk memastikan lulusan siap kerja di industri?",
            "Bisakah Anda menjelaskan peluang karier bagi mahasiswa lulusan program Desain Komunikasi Visual di BINUS University, terutama di bidang animasi?" : "Bisakah Anda menjelaskan peluang [[PROSPECTIVE CAREER]] bagi mahasiswa lulusan [6[VISUAL COMMUNICATION DESIGN]] di BINUS University, terutama di bidang [3[ANIMASI]]?",
            "Bagaimana program International Business Management di BINUS University mempersiapkan mahasiswa untuk berkarier di perusahaan multinasional?" : "Bagaimana [6[INTERNATIONAL BUSINESS MANAGEMENT]] di BINUS University mempersiapkan mahasiswa untuk [[PROSPECTIVE CAREER]] di perusahaan multinasional?",
            "Bagaimana prospek karier sebagai konsultan pajak setelah lulus dari program Perpajakan di BINUS University?" : "Bagaimana [[PROSPECTIVE CAREER]] sebagai konsultan pajak setelah lulus dari [6[TAXATION]] di BINUS University?",
            "Apa perbedaan utama antara program Bisnis Digital di BINUS University dengan program bisnis tradisional dalam hal hasil karier?" : "Apa perbedaan utama antara [6[DIGITAL BUSINESS]] di BINUS University dengan [6[TRADITIONAL BUSINESS]] dalam hal hasil [[PROSPECTIVE CAREER]]?",
            "Apa peran program enrichment seperti magang dan kunjungan lapangan dalam kurikulum program Desain Interior di BINUS University?" : "Apa peran program [[ENRICHMENT]] seperti magang dan kunjungan lapangan dalam kurikulum [6[INTERIOR DESIGN]] di BINUS University?",
            "Bisakah Anda memberikan gambaran tentang bagaimana program Desain Komunikasi Visual di BINUS University mengintegrasikan budaya lokal dan teknologi dalam kurikulumnya?" : "Bisakah Anda memberikan [[PROGRAM DESCRIPTION]] tentang bagaimana [6[VISUAL COMMUNICATION DESIGN]] di BINUS University mengintegrasikan budaya lokal dan teknologi dalam kurikulumnya?",
            "Keterampilan dan pengetahuan apa saja yang akan dikembangkan oleh mahasiswa dalam program Bisnis Digital di BINUS University untuk menjadi pengusaha digital yang sukses?" : "Keterampilan dan pengetahuan apa saja yang akan dikembangkan oleh mahasiswa dalam [6[DIGITAL BUSINESS]] di BINUS University untuk menjadi pengusaha digital yang sukses?",

            "Akreditasi apa yang dimiliki oleh program Perpajakan di BINUS University?" : "[[ACCREDITATION]] apa yang dimiliki oleh [6[TAXATION]] di BINUS University?",
            "Karier potensial apa saja yang bisa diambil oleh lulusan program Akuntansi di BINUS University?" : "[[PROSPECTIVE CAREER]] potensial apa saja yang bisa diambil oleh lulusan [6[ACCOUNTING]] di BINUS University?",
            "Berapa lama waktu yang dibutuhkan untuk menyelesaikan program Fashion di BINUS University?" : "Berapa [[DURATION]] waktu yang dibutuhkan untuk menyelesaikan program [6[FASHION]] di BINUS University?",
            "Gelar akademik apa yang diberikan kepada lulusan program Desain Interior di BINUS University?" : "[0[ACADEMIC TITLE]] akademik apa yang diberikan kepada lulusan [6[INTERIOR DESIGN]] di BINUS University?",
            "Apa saja peluang karier di bidang bisnis digital setelah lulus dari BINUS University?" : "Apa saja peluang [[PROSPECTIVE CAREER]] di bidang [3[DIGITAL BUSINESS]] setelah lulus dari BINUS University?",
            "Bagaimana status akreditasi program Desain Komunikasi Visual di BINUS University?" : "Bagaimana status [[ACCREDITATION]] program [6[VISUAL COMMUNICAITON DESIGN]] di BINUS University?",
            "Jalur karier apa saja yang tersedia bagi lulusan program Fashion di BINUS University?" : "Jalur [[PROSPECTIVE CAREER]] apa saja yang tersedia bagi lulusan program [6[FASHION]] di BINUS University?",
            "Bagaimana program International Business Management di BINUS University mempersiapkan mahasiswa untuk karier global?" : "Bagaimana [6[INTERNATION BUSINESS MANAGEMENT]] di BINUS University mempersiapkan mahasiswa untuk [0[PROSPECTIVE CAREER]] global?",
            "Karier potensial apa saja yang tersedia bagi lulusan program Perpajakan di BINUS University?" : "[0[Karier]] potensial apa saja yang tersedia bagi lulusan [6[TAXATION]] di BINUS University?",
            "Berapa lama durasi program Akuntansi di BINUS University?" : "Berapa lama [[DURATION]] [6[ACCOUNTING]] di BINUS University?",

            "Berapa lama durasi program Perpajakan di BINUS University?" : "Berapa [[DURATION]] [6[TAXATION]] di BINUS University?",
            "Akreditasi apa yang dimiliki program Desain Interior di BINUS University?" : "[[ACCREDITATION]] apa yang dimiliki [6[INTERIOR DESIGN]] di BINUS University?",
            "Gelar akademik apa yang diberikan kepada lulusan Fashion di BINUS University?" : "[[ACADEMIC TITLE]] akademik apa yang diberikan kepada lulusan [3[FASHION]] di BINUS University?",
            "Gelar apa yang Anda dapatkan dari program Bisnis Digital di BINUS University?" : "[[ACADEMIC TITLE]] apa yang Anda dapatkan dari [6[DIGITAL BUSINESS]] di BINUS University?",
            "Apa saja karier potensial untuk lulusan Desain Komunikasi Visual BINUS University?" : "Apa saja [0[karier]] potensial untuk lulusan [3[VISUAL COMMUNICATION DESIGN]] BINUS University?",
            "Apa prospek karier untuk lulusan Fashion BINUS University?" : "Apa prospek [[PROSPECTIVE CAREER]] untuk lulusan [3[FASHION]] BINUS University?",
            "Apa akreditasi program Film di BINUS University?" : "Apa [[ACCREDITATION]] [[FILM]] di BINUS University?",
            "Berapa lama program Film di BINUS University?" : "Berapa [[DURATION]] [6[FILM]] di BINUS University?",
            "Gelar akademik apa yang diberikan kepada lulusan Akuntansi di BINUS University?" : "[0[ACADEMIC TITLE]] akademik apa yang diberikan kepada lulusan [3[ACCOUNTING]] di BINUS University?",
            "Apa pilihan karier bagi lulusan program Animasi di BINUS University?" : "Apa pilihan [[PROSPECTIVE CAREER]] bagi lulusan program [6[ANIMATION]] di BINUS University?"
        }
        return text

    def make_level(self):
        text = self.temporary_knowledge()
        grouped_keys = defaultdict(list)

        for item in text.items():
            for level, pattern in self.level_patterns.items():
                matches = re.findall(pattern, item[0])
                if matches:
                    grouped_keys[level].extend(matches)
                else:
                    grouped_keys[level].append(None)
            grouped_keys["val"].append(item[1])

        return dict(grouped_keys)

    def make_condition(self,inputs):

        condition = ""
        for level, pattern in self.level_patterns.items():
            matches = re.findall(pattern, inputs)
            if matches:
                matches = [match.replace("'", "''") for match in matches]
                if len(matches) > 1:
                    cond = " OR ".join(f"'{match}'" for match in matches)
                    condition += f"AND ({level} IN ({cond})) "
                else:
                    cond = matches[0]
                    condition += f"AND {level} = '{cond}' "

        return condition


x = KnowledgeHandler()
print(x.make_level())
